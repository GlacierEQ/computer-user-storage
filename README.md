# Computer User Storage

**Repository-local health-snapshot and metrics-definition reference.**

This public repository preserves a small Phase 1 observability experiment. It does **not** establish a deployed distributed-storage backend, live PRIMORDIAL MESH runtime, private-record store, legal/case integration, production telemetry pipeline, or external monitoring service.

## Verified capability

[`phase1/health_check_framework.py`](phase1/health_check_framework.py) provides:

- typed caller-supplied component observations;
- validation for status, latency, utilization, and timezone-aware timestamps;
- deterministic aggregate health classification;
- a fail-closed historical `check_mesh_health()` API that reports unavailable when no observation provider is configured.

Every real snapshot emits:

`LOCAL_HEALTH_SNAPSHOT_NOT_DEPLOYMENT_TELEMETRY`

[`phase1/metrics_config.yaml`](phase1/metrics_config.yaml) is a **definition file** containing metric names, units, thresholds, and targets. Those definitions do not prove that a backend currently collects or satisfies them.

## Example

```python
from datetime import UTC, datetime
from phase1.health_check_framework import ComponentObservation, HealthCheckFramework

health = HealthCheckFramework()
result = health.snapshot(
    {
        "local_cache": ComponentObservation(
            status="healthy",
            latency_ms=4.2,
            utilization=0.30,
        )
    },
    observed_at=datetime(2026, 8, 9, tzinfo=UTC),
)
print(result)
```

No network access occurs in this example.

## Native proof

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q phase1 tests
```

The Public Truth Gate runs the exact source head on Python 3.11 and 3.13, parses the YAML metrics configuration, and rejects public case-specific identifiers or fabricated operational/performance claims.

## Evidence and privacy boundary

This repository does **not** claim:

- live storage deployment or synchronization;
- production uptime, throughput, p50/p95/p99 latency, or failover performance;
- live memory/token/resource/forensic/legal automation component health;
- collection of private case, legal, evidence, personal, credential, or account data;
- active stealth-team, evidence-manager, or legal-automation processes;
- external-service, sibling-repository, or provider connectivity;
- that metric targets are measured results.

Public storage/observability examples must remain generic. Case-specific identifiers and private evidence metrics are outside this repository's public projection boundary.

## Preserved history

`PHASE1_FOUNDATION_README.md` and `phase1/DEPLOYMENT_GUIDE.md` document the original Phase 1 idea, but their current text is bounded to experiment/reference status. Historical Git commits remain provenance and must not be interpreted as current deployment evidence.
