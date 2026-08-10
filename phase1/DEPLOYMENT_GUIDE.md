# Phase 1 Local Verification Guide

## Scope

This Phase 1 directory is a **repository-local observability experiment**, not a deployment receipt. It contains a caller-supplied health snapshot helper and a metrics-definition YAML file.

## Components

### Health snapshot framework

`phase1/health_check_framework.py`

- validates explicit component observations;
- aggregates status deterministically;
- rejects invalid latency/utilization/timestamps;
- performs no network discovery;
- returns an explicit unavailable state from the historical `check_mesh_health()` API when no observation provider is configured.

### Metrics definitions

`phase1/metrics_config.yaml`

- defines generic metric names, units, thresholds, and targets;
- does not establish collection, monitoring, deployment, uptime, performance, encryption coverage, or private-data integration.

## Local verification

```bash
python -m compileall -q phase1 tests
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Nonclaims

These files do not establish:

- a live distributed-storage backend;
- PRIMORDIAL MESH deployment;
- live stealth-team/core-component health;
- production p50/p95/p99 latency or throughput;
- failover performance;
- legal/evidence/case tracking;
- private-record access;
- provider or sibling-repository integration.

Historical deployment-oriented wording is preserved in Git provenance only. Current public promotion is limited to the verified local code and generic metric definitions.
