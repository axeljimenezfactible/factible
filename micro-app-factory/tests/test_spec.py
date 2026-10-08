"""Pruebas del validador. Los datos de las pruebas unitarias son fixtures sintéticos."""
import copy
import glob
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)

import spec  # noqa: E402

CATALOG = spec.load_catalog()


def base_spec(**overrides):
    data = {
        "id": "demo-app",
        "name": "Demo",
        "source_candidate": "demo",
        "platforms": ["windows", "mac"],
        "price_usd": 29,
        "license_model": "perpetual",
        "privacy": {"processes_locally": True, "network_calls": ["license", "update"]},
        "modules": [{"id": "doc.pdf"}, {"id": "io.files"}],
        "flow": ["a", "b", "c"],
        "review_required": False,
        "golden_tests": [{"name": f"t{i}", "description": "d"} for i in range(3)],
        "risks": ["r"],
        "validation": {"fake_door_prices_usd": [19], "status": "pendiente"},
    }
    data.update(overrides)
    return data


class ValidateTests(unittest.TestCase):
    def errors(self, **overrides):
        return spec.validate(base_spec(**overrides), CATALOG)

    def test_valid_spec_has_no_errors(self):
        self.assertEqual(self.errors(), [])

    def test_missing_field(self):
        data = base_spec()
        del data["risks"]
        self.assertIn("falta el campo 'risks'", spec.validate(data, CATALOG))

    def test_bad_slug(self):
        self.assertTrue(any("slug" in e for e in self.errors(id="Demo App")))

    def test_unknown_module(self):
        self.assertTrue(any("desconocido" in e for e in self.errors(modules=[{"id": "no.existe"}])))

    def test_core_module_is_implicit(self):
        self.assertTrue(any("núcleo" in e for e in self.errors(modules=[{"id": "core.shell"}])))

    def test_platform_not_covered_by_module(self):
        errs = self.errors(platforms=["mac"], modules=[{"id": "capture.input_win"}])
        self.assertTrue(any("no cubre" in e for e in errs))

    def test_duplicate_modules(self):
        self.assertTrue(any("repetidos" in e for e in self.errors(modules=[{"id": "doc.pdf"}, {"id": "doc.pdf"}])))

    def test_partial_result_module_requires_review(self):
        errs = self.errors(modules=[{"id": "vision.ocr"}], review_required=False)
        self.assertTrue(any("review_required" in e for e in errs))
        self.assertTrue(any("review.ui" in e for e in errs))

    def test_partial_result_module_ok_with_review(self):
        errs = self.errors(modules=[{"id": "vision.ocr"}, {"id": "review.ui"}], review_required=True)
        self.assertEqual(errs, [])

    def test_network_call_not_allowed(self):
        privacy = {"processes_locally": True, "network_calls": ["license", "subir_archivos"]}
        self.assertTrue(any("network_calls" in e for e in self.errors(privacy=privacy)))

    def test_must_process_locally(self):
        privacy = {"processes_locally": False, "network_calls": ["license"]}
        self.assertTrue(any("processes_locally" in e for e in self.errors(privacy=privacy)))

    def test_needs_three_golden_tests(self):
        tests = [{"name": "a", "description": "d"}, {"name": "b", "description": "d"}]
        self.assertTrue(any("golden_tests" in e for e in self.errors(golden_tests=tests)))

    def test_price_bounds(self):
        self.assertTrue(any("price_usd" in e for e in self.errors(price_usd=0)))
        self.assertTrue(any("price_usd" in e for e in self.errors(price_usd=500)))
        self.assertTrue(any("price_usd" in e for e in self.errors(price_usd=True)))

    def test_bad_validation_status(self):
        bad = {"fake_door_prices_usd": [19], "status": "quizá"}
        self.assertTrue(any("status" in e for e in self.errors(validation=bad)))

    def test_wrong_types_do_not_crash(self):
        errs = self.errors(platforms="windows", modules="doc.pdf", flow=3, golden_tests=None)
        self.assertTrue(errs)


class ExampleSpecTests(unittest.TestCase):
    def setUp(self):
        self.paths = sorted(glob.glob(os.path.join(ROOT, "specs", "*.json")))

    def test_example_specs_exist_and_are_valid(self):
        import json
        self.assertGreaterEqual(len(self.paths), 4)
        for path in self.paths:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            self.assertEqual(spec.validate(data, CATALOG), [], os.path.basename(path))
            self.assertEqual(data["id"], os.path.splitext(os.path.basename(path))[0])


class ReportTests(unittest.TestCase):
    def test_shared_modules_come_first(self):
        a = base_spec(modules=[{"id": "doc.pdf"}, {"id": "io.files"}])
        b = base_spec(id="otra", modules=[{"id": "doc.pdf"}, {"id": "data.tables"}])
        counts, shared, single = spec.usage_report([a, b])
        self.assertEqual(shared, [("doc.pdf", 2)])
        self.assertEqual(single, ["data.tables", "io.files"])
        self.assertEqual(counts["doc.pdf"], 2)

    def test_report_does_not_mutate_specs(self):
        a = base_spec()
        before = copy.deepcopy(a)
        spec.usage_report([a])
        self.assertEqual(a, before)


if __name__ == "__main__":
    unittest.main()
