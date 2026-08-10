from __future__ import annotations

from datetime import UTC, datetime
import math
import unittest

from phase1.health_check_framework import ComponentObservation, HealthCheckFramework


class TestHealthCheckFramework(unittest.TestCase):
    def test_snapshot_aggregates_caller_supplied_health(self) -> None:
        framework = HealthCheckFramework()
        result = framework.snapshot(
            {
                "cache": ComponentObservation("healthy", latency_ms=4.5, utilization=0.2),
                "index": ComponentObservation("degraded", latency_ms=9.0, utilization=0.8),
            },
            observed_at=datetime(2026, 8, 9, tzinfo=UTC),
        )
        self.assertEqual(result["status"], "degraded")
        self.assertEqual(
            result["evidence_state"],
            "LOCAL_HEALTH_SNAPSHOT_NOT_DEPLOYMENT_TELEMETRY",
        )
        self.assertEqual(result["components"]["cache"]["latency_ms"], 4.5)
        self.assertNotIn("performance", result)
        self.assertNotIn("legal_automation", str(result))

    def test_historical_check_is_explicitly_unavailable(self) -> None:
        result = HealthCheckFramework().check_mesh_health()
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["components"], {})
        self.assertEqual(result["reason"], "NO_OBSERVATION_PROVIDER_CONFIGURED")

    def test_invalid_observations_fail_closed(self) -> None:
        for status in ("operational", "running", "perfect"):
            with self.assertRaises(ValueError):
                ComponentObservation(status)
        for latency in (-1.0, math.nan, math.inf):
            with self.assertRaises(ValueError):
                ComponentObservation("healthy", latency_ms=latency)
        for utilization in (-0.1, 1.1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                ComponentObservation("healthy", utilization=utilization)

    def test_snapshot_requires_timezone_aware_timestamp(self) -> None:
        with self.assertRaises(ValueError):
            HealthCheckFramework().snapshot(
                {"cache": ComponentObservation("healthy")},
                observed_at=datetime(2026, 8, 9),
            )

    def test_framework_configuration_validation(self) -> None:
        with self.assertRaises(ValueError):
            HealthCheckFramework(0)
        with self.assertRaises(TypeError):
            HealthCheckFramework(True)
        with self.assertRaises(ValueError):
            HealthCheckFramework().snapshot({})


if __name__ == "__main__":
    unittest.main()
