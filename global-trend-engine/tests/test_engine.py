"""Pruebas del motor. Los candidatos de aquí son fixtures sintéticos de prueba, no datos de mercado."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import faketest  # noqa: E402
import score  # noqa: E402


def candidate(**overrides):
    base = {
        "id": "fixture",
        "region": "US",
        "pain_point": "p",
        "evidence": [{"url": "https://a.example/x"}, {"url": "https://www.b.example/y"}],
        "paid_alternatives": [
            {"name": "Alt1", "price_usd": 19, "model": "one-time"},
            {"name": "Alt2", "price_usd": 4, "model": "monthly"},
        ],
        "search_signals": {"queries": ["q1", "q2"], "volume_note": None},
        "urgency_1to5": 4,
        "buildability_1to5": 4,
        "wtp_20_evidence": "x",
        "confidence": "high",
    }
    base.update(overrides)
    return base


class ScoreTests(unittest.TestCase):
    def test_price_anchor_ranges(self):
        self.assertTrue(score.is_price_anchor({"price_usd": 20, "model": "one-time"}))
        self.assertFalse(score.is_price_anchor({"price_usd": 500, "model": "one-time"}))
        self.assertFalse(score.is_price_anchor({"price_usd": None, "model": "one-time"}))
        self.assertFalse(score.is_price_anchor({"price_usd": True, "model": "one-time"}))
        self.assertFalse(score.is_price_anchor({"price_usd": 20, "model": "freemium"}))

    def test_evidence_counts_distinct_domains_and_ignores_www(self):
        c = candidate(evidence=[{"url": "https://a.example/1"}, {"url": "https://www.a.example/2"}])
        self.assertEqual(score.evidence_strength(c), 0.25)

    def test_more_anchors_raise_score(self):
        few = candidate(paid_alternatives=[{"name": "A", "price_usd": 19, "model": "one-time"}])
        many = candidate()
        self.assertGreater(score.score_candidate(many)["score"], score.score_candidate(few)["score"])

    def test_low_confidence_lowers_score(self):
        hi = score.score_candidate(candidate(confidence="high"))["score"]
        lo = score.score_candidate(candidate(confidence="low"))["score"]
        self.assertLess(lo, hi)

    def test_free_alternatives_lower_score(self):
        free = [{"name": f"F{i}", "price_usd": 0, "model": "freemium"} for i in range(3)]
        base = candidate()
        crowded = candidate(paid_alternatives=base["paid_alternatives"] + free)
        self.assertEqual(score.score_candidate(crowded)["free_alts"], 3)
        self.assertLess(score.score_candidate(crowded)["score"], score.score_candidate(base)["score"])

    def test_free_alternatives_penalty_is_capped(self):
        many = [{"name": f"F{i}", "price_usd": 0, "model": "freemium"} for i in range(10)]
        three = many[:3]
        a = score.score_candidate(candidate(paid_alternatives=three))["score"]
        b = score.score_candidate(candidate(paid_alternatives=many))["score"]
        self.assertEqual(a, b)

    def test_missing_fields_do_not_crash_and_are_flagged(self):
        r = score.score_candidate({"id": "vacio"})
        self.assertGreaterEqual(r["score"], 0)
        for gap in ("urgency", "buildability", "no_price_anchor", "no_search_volume"):
            self.assertIn(gap, r["gaps"])

    def test_score_in_range(self):
        r = score.score_candidate(candidate())
        self.assertTrue(0 <= r["score"] <= 100)


class FakeDoorTests(unittest.TestCase):
    def test_required_rate(self):
        self.assertAlmostEqual(faketest.required_intent_rate(0.3, 9.0, 0.3), 0.3 / 9 / 0.3)

    def test_go_when_clearly_above(self):
        self.assertEqual(faketest.decide(1000, 200, cpc=0.3)["verdict"], "GO")

    def test_discard_when_clearly_below(self):
        self.assertEqual(faketest.decide(1000, 5, cpc=0.3)["verdict"], "DESCARTAR")

    def test_small_sample_always_continues(self):
        self.assertEqual(faketest.decide(100, 90, cpc=0.3)["verdict"], "CONTINUAR")

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            faketest.decide(10, 20, cpc=0.3)
        with self.assertRaises(ValueError):
            faketest.required_intent_rate(0.3, 0, 0.3)

    def test_reproducible(self):
        self.assertEqual(faketest.decide(1000, 120, cpc=0.3), faketest.decide(1000, 120, cpc=0.3))


if __name__ == "__main__":
    unittest.main()
