"""Repository-local health snapshot primitives for Computer User Storage.

The original Phase 1 file returned hard-coded operational, performance, legal,
and evidence counts as if they were live telemetry. This module now requires
callers to provide observations explicitly and labels the result as a local
snapshot. It performs no network access and reads no private records.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import math
from typing import Any, Mapping

EVIDENCE_STATE = "LOCAL_HEALTH_SNAPSHOT_NOT_DEPLOYMENT_TELEMETRY"
_ALLOWED = {"healthy", "degraded", "unavailable", "unknown"}


@dataclass(frozen=True)
class ComponentObservation:
    status: str
    latency_ms: float | None = None
    utilization: float | None = None

    def __post_init__(self) -> None:
        if self.status not in _ALLOWED:
            raise ValueError(f"unsupported status: {self.status}")
        if self.latency_ms is not None:
            latency = float(self.latency_ms)
            if not math.isfinite(latency) or latency < 0:
                raise ValueError("latency_ms must be finite and >= 0")
        if self.utilization is not None:
            utilization = float(self.utilization)
            if not math.isfinite(utilization) or not 0 <= utilization <= 1:
                raise ValueError("utilization must be finite and within [0, 1]")


class HealthCheckFramework:
    """Aggregate caller-supplied local observations without inventing telemetry."""

    def __init__(self, check_interval: int = 30) -> None:
        if isinstance(check_interval, bool) or not isinstance(check_interval, int):
            raise TypeError("check_interval must be an integer")
        if check_interval < 1:
            raise ValueError("check_interval must be positive")
        self.check_interval = check_interval

    def snapshot(
        self,
        components: Mapping[str, ComponentObservation],
        *,
        observed_at: datetime | None = None,
    ) -> dict[str, Any]:
        if not components:
            raise ValueError("at least one component observation is required")
        normalized: dict[str, dict[str, Any]] = {}
        for name, observation in sorted(components.items()):
            if not name.strip():
                raise ValueError("component names must not be empty")
            if not isinstance(observation, ComponentObservation):
                raise TypeError("components must contain ComponentObservation values")
            item: dict[str, Any] = {"status": observation.status}
            if observation.latency_ms is not None:
                item["latency_ms"] = float(observation.latency_ms)
            if observation.utilization is not None:
                item["utilization"] = float(observation.utilization)
            normalized[name] = item

        statuses = {item["status"] for item in normalized.values()}
        if "unavailable" in statuses:
            overall = "unavailable"
        elif "degraded" in statuses:
            overall = "degraded"
        elif statuses == {"healthy"}:
            overall = "healthy"
        else:
            overall = "unknown"

        timestamp = observed_at or datetime.now(UTC)
        if timestamp.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")

        return {
            "observed_at": timestamp.astimezone(UTC).isoformat(),
            "status": overall,
            "components": normalized,
            "evidence_state": EVIDENCE_STATE,
        }

    def check_mesh_health(self) -> dict[str, Any]:
        """Historical API retained as an explicit fail-closed unconfigured result."""

        return {
            "status": "unavailable",
            "components": {},
            "evidence_state": EVIDENCE_STATE,
            "reason": "NO_OBSERVATION_PROVIDER_CONFIGURED",
        }
