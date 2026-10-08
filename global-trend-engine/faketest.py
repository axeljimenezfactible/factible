"""Calculadora de pruebas de "puerta falsa" (landing + anuncio) para un nicho.

Modelo Beta-Binomial: tras n visitas con k intenciones de compra (clic a
checkout o registro con el precio visible), estima la probabilidad de que la
conversión real supere la mínima que paga el CAC objetivo. Solo biblioteca
estándar; el muestreo usa semilla fija para ser reproducible.

Supuestos explícitos (calibrarlos con datos reales de las primeras pruebas):
  - haircut: fracción de la intención medida que termina en compra real.
  - prior Beta(1, 30): débil, centrado en ~3% de intención.
"""
import argparse
import random
import sys


def required_intent_rate(cpc, cac_target, haircut):
    """Tasa de intención mínima para que CPC / (tasa * haircut) <= CAC objetivo."""
    if cpc < 0 or cac_target <= 0 or not 0 < haircut <= 1:
        raise ValueError("cpc>=0, cac_target>0 y 0<haircut<=1")
    return cpc / cac_target / haircut


def posterior_above(n, k, p_min, prior=(1.0, 30.0), draws=20000, seed=7):
    """P(tasa real > p_min) e intervalo creíble al 90% (percentiles 5 y 95)."""
    if n < 0 or not 0 <= k <= n:
        raise ValueError("se requiere 0 <= k <= n")
    a, b = prior[0] + k, prior[1] + (n - k)
    rng = random.Random(seed)
    xs = sorted(rng.betavariate(a, b) for _ in range(draws))
    prob = sum(x > p_min for x in xs) / draws
    return prob, (xs[int(0.05 * draws)], xs[int(0.95 * draws) - 1])


def decide(n, k, cpc, cac_target=9.0, haircut=0.3, min_n=300, go=0.9, kill=0.1):
    p_min = required_intent_rate(cpc, cac_target, haircut)
    prob, interval = posterior_above(n, k, p_min)
    if n < min_n:
        verdict, why = "CONTINUAR", f"muestra insuficiente (n={n} < {min_n})"
    elif prob >= go:
        verdict, why = "GO", f"P(tasa > mínima) = {prob:.2f} >= {go}"
    elif prob <= kill:
        verdict, why = "DESCARTAR", f"P(tasa > mínima) = {prob:.2f} <= {kill}"
    else:
        verdict, why = "CONTINUAR", f"evidencia ambigua, P = {prob:.2f}"
    return {
        "verdict": verdict,
        "reason": why,
        "p_min": round(p_min, 4),
        "prob_above": round(prob, 3),
        "interval90": (round(interval[0], 4), round(interval[1], 4)),
        "observed": round(k / n, 4) if n else None,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--visits", type=int, required=True)
    ap.add_argument("--intents", type=int, required=True)
    ap.add_argument("--cpc", type=float, required=True, help="costo por clic en USD")
    ap.add_argument("--cac-target", type=float, default=9.0)
    ap.add_argument("--haircut", type=float, default=0.3)
    args = ap.parse_args(argv)
    result = decide(args.visits, args.intents, args.cpc, args.cac_target, args.haircut)
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
