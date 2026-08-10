from __future__ import annotations

from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class TestPublicSurface(unittest.TestCase):
    def test_metrics_yaml_is_generic_and_parseable(self) -> None:
        text = (ROOT / "phase1" / "metrics_config.yaml").read_text(encoding="utf-8")
        payload = yaml.safe_load(text)
        self.assertIsInstance(payload, dict)
        self.assertIn("metrics", payload)
        self.assertNotIn("case", text.lower())
        self.assertNotIn("evidence_items", text)

    def test_current_public_files_exclude_case_specific_identifiers(self) -> None:
        for relative in (
            "README.md",
            "PHASE1_FOUNDATION_README.md",
            "phase1/DEPLOYMENT_GUIDE.md",
            "phase1/metrics_config.yaml",
            "phase1/health_check_framework.py",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("1FDV", text)
            self.assertNotIn("legal_automation", text)
            self.assertNotIn("evidence_manager", text)

    def test_readme_exposes_fail_closed_evidence_token(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        source = (ROOT / "phase1" / "health_check_framework.py").read_text(
            encoding="utf-8"
        )
        token = "LOCAL_HEALTH_SNAPSHOT_NOT_DEPLOYMENT_TELEMETRY"
        self.assertIn(token, readme)
        self.assertIn(token, source)
        self.assertIn("does **not** establish", readme)


if __name__ == "__main__":
    unittest.main()
