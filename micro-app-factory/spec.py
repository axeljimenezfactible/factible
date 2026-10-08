"""Validador de especificaciones de micro-apps (Fase 2). Solo biblioteca estándar.

Una especificación declara qué módulos del catálogo usa una micro-app, en qué
plataformas corre, cómo cuida la privacidad y cómo se prueba. El validador
aplica las reglas de la fábrica; el informe de uso dice qué módulos conviene
construir primero (los que comparten dos o más apps).
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(HERE, "catalog.json")
PLATFORMS = {"windows", "mac", "linux"}
LICENSE_MODELS = {"perpetual", "perpetual+12m-updates"}
NETWORK_CALLS = {"license", "update", "telemetry_optin"}
STATUSES = {"pendiente", "en_curso", "go", "descartar"}
REQUIRED = (
    "id", "name", "source_candidate", "platforms", "price_usd", "license_model",
    "privacy", "modules", "flow", "review_required", "golden_tests", "risks", "validation",
)
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_catalog(path=CATALOG_PATH):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    modules = {m["id"]: m for m in data["modules"]}
    if len(modules) != len(data["modules"]):
        raise ValueError("ids de módulo duplicados en el catálogo")
    return modules


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _nonempty_strings(items):
    return isinstance(items, list) and items and all(isinstance(s, str) and s.strip() for s in items)


def validate(spec, catalog):
    """Devuelve la lista de errores de la especificación (vacía si es válida)."""
    errors = [f"falta el campo '{key}'" for key in REQUIRED if key not in spec]
    if errors:
        return errors

    if not (isinstance(spec["id"], str) and SLUG.match(spec["id"])):
        errors.append("id debe ser un slug en minúsculas con guiones")

    platforms = spec["platforms"]
    platforms_ok = isinstance(platforms, list) and bool(platforms) and set(platforms) <= PLATFORMS
    if not platforms_ok:
        errors.append(f"platforms debe ser una lista no vacía dentro de {sorted(PLATFORMS)}")

    if not (_is_number(spec["price_usd"]) and 0 < spec["price_usd"] <= 200):
        errors.append("price_usd debe ser un número mayor que 0 y de hasta 200")

    if spec["license_model"] not in LICENSE_MODELS:
        errors.append(f"license_model debe ser uno de {sorted(LICENSE_MODELS)}")

    privacy = spec["privacy"]
    if not isinstance(privacy, dict):
        errors.append("privacy debe ser un objeto")
    else:
        if privacy.get("processes_locally") is not True:
            errors.append("privacy.processes_locally debe ser true")
        calls = privacy.get("network_calls")
        if not isinstance(calls, list) or not set(calls) <= NETWORK_CALLS:
            errors.append(f"privacy.network_calls debe ser una lista dentro de {sorted(NETWORK_CALLS)}")

    ids = []
    modules = spec["modules"]
    if not isinstance(modules, list) or not modules:
        errors.append("modules debe ser una lista no vacía")
    else:
        for module in modules:
            module_id = module.get("id") if isinstance(module, dict) else None
            if not module_id:
                errors.append("cada módulo necesita 'id'")
                continue
            ids.append(module_id)
            entry = catalog.get(module_id)
            if entry is None:
                errors.append(f"módulo desconocido: {module_id}")
            elif entry.get("core"):
                errors.append(f"{module_id} es del núcleo y se incluye de forma implícita")
            elif platforms_ok and not set(platforms) <= set(entry["platforms"]):
                missing = sorted(set(platforms) - set(entry["platforms"]))
                errors.append(f"{module_id} no cubre las plataformas {missing}")
        duplicated = sorted(k for k, v in Counter(ids).items() if v > 1)
        if duplicated:
            errors.append(f"módulos repetidos: {duplicated}")
        if any(catalog.get(i, {}).get("requires_review") for i in ids):
            if spec["review_required"] is not True:
                errors.append("usa un módulo de resultado parcial: review_required debe ser true")
            if "review.ui" not in ids:
                errors.append("usa un módulo de resultado parcial: debe incluir review.ui")

    if not _nonempty_strings(spec["flow"]) or len(spec["flow"]) < 3:
        errors.append("flow necesita al menos 3 pasos de texto")

    tests = spec["golden_tests"]
    valid_tests = isinstance(tests, list) and all(
        isinstance(t, dict) and str(t.get("name", "")).strip() and str(t.get("description", "")).strip()
        for t in tests
    )
    if not (valid_tests and len(tests) >= 3):
        errors.append("golden_tests necesita al menos 3 pruebas con name y description")

    if not _nonempty_strings(spec["risks"]):
        errors.append("risks necesita al menos un riesgo de texto")

    validation = spec["validation"]
    prices = validation.get("fake_door_prices_usd") if isinstance(validation, dict) else None
    if not (isinstance(prices, list) and prices and all(_is_number(p) and p > 0 for p in prices)):
        errors.append("validation.fake_door_prices_usd debe ser una lista de precios mayores que 0")
    if not isinstance(validation, dict) or validation.get("status") not in STATUSES:
        errors.append(f"validation.status debe ser uno de {sorted(STATUSES)}")

    return errors


def usage_report(specs):
    """Cuenta cuántas especificaciones usan cada módulo y propone el orden de construcción."""
    counts = Counter()
    for spec in specs:
        counts.update({m["id"] for m in spec["modules"]})
    shared = sorted(((m, c) for m, c in counts.items() if c >= 2), key=lambda x: (-x[1], x[0]))
    single = sorted(m for m, c in counts.items() if c == 1)
    return counts, shared, single


def _load_specs(paths):
    specs = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            specs.append((path, json.load(fh)))
    return specs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["validate", "report"])
    ap.add_argument("specs", nargs="+", help="archivos JSON de especificación")
    ap.add_argument("--catalog", default=CATALOG_PATH)
    args = ap.parse_args(argv)
    catalog = load_catalog(args.catalog)
    loaded = _load_specs(args.specs)

    if args.command == "validate":
        failed = 0
        for path, spec in loaded:
            errors = validate(spec, catalog)
            print(f"{'OK    ' if not errors else 'ERROR '}{os.path.basename(path)}")
            for err in errors:
                print(f"       - {err}")
            failed += bool(errors)
        return 1 if failed else 0

    valid = [spec for _, spec in loaded if not validate(spec, catalog)]
    counts, shared, single = usage_report(valid)
    print(f"Especificaciones válidas: {len(valid)} de {len(loaded)}")
    print("\nConstruir primero (módulos compartidos por 2 o más apps):")
    for module_id, count in shared:
        print(f"  {count} apps  {module_id}")
    print("\nEspecíficos de una sola app (no construir como módulo hasta que lo use otra):")
    for module_id in single:
        print(f"  {module_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
