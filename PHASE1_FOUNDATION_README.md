# Phase 1 Foundation — Storage / Observability Experiment

This directory preserves an early local observability experiment: a health-snapshot helper plus metrics definitions.

## Current boundary

- The health framework accepts **caller-supplied local observations**; it does not discover or monitor a live mesh.
- The metrics YAML defines names, units, thresholds, and targets; it does not prove telemetry collection or target attainment.
- No private case, legal, evidence, personal, credential, or account data belongs in this public repository.
- No live PRIMORDIAL MESH, stealth-team, storage backend, provider integration, or deployment is established by these files.

Use the root [`README.md`](README.md) as the canonical public front door and `phase1/health_check_framework.py` as the current executable surface.
