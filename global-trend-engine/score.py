"""Puntuación v0 de nichos del Global Trend Engine (solo biblioteca estándar).

Lee uno o más JSON con candidatos (esquema de la Fase 1), calcula un puntaje
0-100 por media geométrica ponderada y marca los huecos de datos. La demanda
es un *proxy* débil mientras no haya volúmenes de búsqueda reales (DataForSEO,
Google Trends API).
"""
import argparse
import csv
import json
import math
import sys
from urllib.parse import urlparse

WEIGHTS = {"evidence": 0.15, "payment": 0.30, "urgency": 0.20, "build": 0.20, "demand": 0.15}
CONFIDENCE = {"low": 0.6, "med": 0.8, "high": 1.0}
FLOOR = 0.05  # evita que un 0 anule todo el puntaje; el hueco se reporta aparte
ANCHOR_BOUNDS = {"one-time": (8, 50), "monthly": (2, 12), "annual": (15, 100)}  # USD


def _domain(url):
    host = urlparse(url or "").netloc.lower()
    return host[4:] if host.startswith("www.") else host


def _scale(value, lo, hi):
    """Lleva value de [lo, hi] a [0, 1]; None si no es un número válido."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return min(max((value - lo) / (hi - lo), 0.0), 1.0)


def is_price_anchor(alt):
    """True si la alternativa de pago tiene un precio en rango de pago creíble."""
    price = alt.get("price_usd")
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return False
    bounds = ANCHOR_BOUNDS.get(alt.get("model"))
    return bool(bounds) and bounds[0] <= price <= bounds[1]


def price_anchors(candidate):
    names = {
        (alt.get("name") or "").strip().lower()
        for alt in candidate.get("paid_alternatives") or []
        if is_price_anchor(alt)
    }
    return {n for n in names if n}


def evidence_strength(candidate):
    domains = {_domain(e.get("url")) for e in candidate.get("evidence") or [] if e.get("url")}
    domains.discard("")
    return min(len(domains), 4) / 4


def payment_score(candidate):
    anchors = min(len(price_anchors(candidate)), 3) / 3
    return 0.7 * anchors + 0.3 * (1.0 if candidate.get("wtp_20_evidence") else 0.0)


def demand_proxy(candidate):
    signals = candidate.get("search_signals") or {}
    queries = [q for q in signals.get("queries") or [] if q]
    return 0.5 * min(len(queries), 5) / 5 + (0.5 if signals.get("volume_note") else 0.0)


def score_candidate(candidate):
    gaps = []
    urgency = _scale(candidate.get("urgency_1to5"), 1, 5)
    build = _scale(candidate.get("buildability_1to5"), 1, 5)
    if urgency is None:
        gaps.append("urgency")
        urgency = 0.5
    if build is None:
        gaps.append("buildability")
        build = 0.5
    parts = {
        "evidence": evidence_strength(candidate),
        "payment": payment_score(candidate),
        "urgency": urgency,
        "build": build,
        "demand": demand_proxy(candidate),
    }
    if not price_anchors(candidate):
        gaps.append("no_price_anchor")
    if not (candidate.get("search_signals") or {}).get("volume_note"):
        gaps.append("no_search_volume")
    total_w = sum(WEIGHTS.values())
    log_mean = sum(WEIGHTS[k] * math.log(max(v, FLOOR)) for k, v in parts.items()) / total_w
    confidence = CONFIDENCE.get(candidate.get("confidence"), CONFIDENCE["low"])
    return {
        "id": candidate.get("id"),
        "region": candidate.get("region"),
        "pain_point": candidate.get("pain_point"),
        "micro_app_idea": candidate.get("micro_app_idea"),
        "score": round(100 * math.exp(log_mean) * confidence, 1),
        **{k: round(v, 2) for k, v in parts.items()},
        "confidence": candidate.get("confidence"),
        "gaps": ";".join(gaps),
    }


def load(paths):
    candidates = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            print(f"aviso: {path} no es una lista de candidatos, se omite", file=sys.stderr)
            continue
        for item in data:
            if isinstance(item, dict) and item.get("id"):
                candidates.append(item)
            else:
                print(f"aviso: candidato sin id en {path}, se omite", file=sys.stderr)
    return candidates


def to_markdown(rows, top):
    lines = ["| # | Región | Dolor | Puntaje | Hueco de datos |", "|---|---|---|---|---|"]
    for i, r in enumerate(rows[:top], 1):
        pain = (r["pain_point"] or "").replace("|", "/")
        lines.append(f"| {i} | {r['region']} | {pain} | {r['score']} | {r['gaps'] or '-'} |")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+", help="JSON(s) con candidatos")
    ap.add_argument("--csv", help="ruta de salida CSV con el ranking completo")
    ap.add_argument("--top", type=int, default=20, help="filas de la tabla Markdown")
    args = ap.parse_args(argv)
    rows = sorted((score_candidate(c) for c in load(args.inputs)), key=lambda r: -r["score"])
    if args.csv and rows:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(to_markdown(rows, args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
