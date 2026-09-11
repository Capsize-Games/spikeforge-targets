# spikeforge-targets

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

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## License

BSD-3-Clause. See [`LICENSE`](LICENSE).
