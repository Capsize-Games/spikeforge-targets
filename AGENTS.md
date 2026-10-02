# SpikeForge targets

This repository owns the `spikeforge_targets` package: deployment-target
adapters, event-driven energy accounting, and optional Norse/Lava backends.
Keep those backend SDKs optional and keep the dependency direction from
targets to `spikeforge` core; the core package must not depend on this package.

The local task contract is `python -m compileall -q spikeforge_targets` for the
build check, `ruff check .` for lint, and `pytest` for tests. Install the
development extra with `pip install -e ".[dev]"` after installing the public
`spikeforge` core dependency as described in `README.md`. CI runs on GitHub-hosted Ubuntu workers. The core dependency is public and
its fallback checkout uses anonymous HTTPS; no deploy key is required.

Norse and Lava are optional backend integrations. Tests that require those
extras must keep their skip/availability behavior explicit; do not claim a
hardware backend check from the CPU-only baseline.
