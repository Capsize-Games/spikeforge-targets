# spikeforge-targets

[![CI](https://github.com/capsize-games/spikeforge-targets/actions/workflows/ci.yml/badge.svg)](https://github.com/capsize-games/spikeforge-targets/actions/workflows/ci.yml)
[![Discord](https://img.shields.io/badge/Discord-Join%20the%20community-5865F2?logo=discord&logoColor=white)](https://capsizegames.com/discord)
[![Status: pre-1.0](https://img.shields.io/badge/status-pre--1.0-orange.svg)](pyproject.toml)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Deployment targets, event-driven energy accounting, and backend execution
adapters for the [spikeforge](https://github.com/capsize-games/spikeforge)
spiking-neural-network interpreter.

`spikeforge-targets` owns the `spikeforge_targets` import root:

- `spikeforge_targets.backends` — execution adapters (reference, norse, lava).
- `spikeforge_targets.energy` — event-driven energy cost accounting and reporting.
- `spikeforge_targets.event_runtime` — sparse/event-driven runtime primitives.
- `spikeforge_targets.cli` / `spikeforge_targets.energy.cli` — the
  `spikeforge-targets` and `spikeforge-energy` console scripts.

## Installation

```bash
pip install spikeforge-targets
```

The optional `norse` and `lava` extras gate the corresponding backend SDKs:

```bash
pip install "spikeforge-targets[norse]"
pip install "spikeforge-targets[lava]"
```

## Release provenance and family compatibility

PyPI `spikeforge-targets` publishes from the monorepo
[Capsize-Games/spikeforge](https://github.com/Capsize-Games/spikeforge)
(`packages/spikeforge-targets`), not from this standalone mirror. The
monorepo `release.yml` publishes `<distribution>-v<version>` tags through a
per-distribution trusted publisher and refuses the tag unless the tag,
`pyproject.toml`, and `compatibility.json` agree and the core pin is exactly
`spikeforge~=<matrix core>`. This checkout tracks that matrix: the core pin
here must stay on the matrix core line (currently `spikeforge~=0.6.3`; see
`docs/release-policy.md` and `docs/fleet-audit.md`). Family owner, supported
Python (`>=3.10`, CI `3.10–3.13` with CPU torch wheels), `torch>=2.5`,
Ruff/pytest floors, and downstream notes (including `999`) live in
[`docs/release-policy.md`](docs/release-policy.md).

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## License

BSD-3-Clause. See [`LICENSE`](LICENSE).

## Citation

`spikeforge-targets` is an extracted component of the
[spikeforge](https://github.com/capsize-games/spikeforge) toolkit and has no
independent research identity of its own — cite the parent project's
`CITATION.cff` instead of adding a second one here.
