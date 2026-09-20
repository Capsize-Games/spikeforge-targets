# SpikeForge targets

This repository owns the `spikeforge_targets` package: deployment-target
adapters, event-driven energy accounting, and optional Norse/Lava backends.
Keep those backend SDKs optional and keep the dependency direction from
targets to `spikeforge` core; the core package must not depend on this package.

The local task contract is `python -m compileall -q spikeforge_targets` for the
build check, `ruff check .` for lint, and `pytest` for tests. Install the
development extra with `pip install -e ".[dev]"` after installing the private
`spikeforge` core dependency as described in `README.md`. CI uses a
repository-scoped local runner and a read-only deploy key for that dependency;
never replace it with a broader credential or commit credential material.

Norse and Lava are optional backend integrations. Tests that require those
extras must keep their skip/availability behavior explicit; do not claim a
hardware backend check from the CPU-only baseline.
