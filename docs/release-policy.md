# Release policy — spikeforge-targets (standalone mirror)

Converges this repository on the shared spikeforge family release policy
for [Capsize-Games/spikeforge-targets#2](https://github.com/Capsize-Games/spikeforge-targets/issues/2).
Verified against `main` here (`0.1.0`) and the monorepo
`Capsize-Games/spikeforge` (`packages/spikeforge-targets` `0.2.4`,
core `spikeforge` `0.6.3`) on 2026-11-25.

## 1. Owner and boundary

- Family owner: Capsize LLC (`contact@capsizegames.com`), BSD-3-Clause.
- This repository owns the `spikeforge_targets` import root:
  deployment-target adapters, event-driven energy accounting,
  quantization, and the optional Norse/Lava backend integrations.
- Dependency direction is targets-to-core: `spikeforge_targets`
  depends on `spikeforge` core; core never depends on targets.
- Optional backend SDKs (`norse`, `lava-nc`) stay optional extras with
  explicit skip/availability behavior; the CPU-only reference path is
  the supported default.

## 2. Release provenance: this repository does not publish

- PyPI `spikeforge-targets` builds from monorepo
  `packages/spikeforge-targets`, not from this standalone checkout.
  This repository has no release workflow and no PyPI trusted
  publisher; the only workflow here is `ci.yml`.
- Fleet-audit evidence (`docs/fleet-audit.md`) records the mirror
  relationship: standalone `0.1.0` versus monorepo `0.2.1` at audit
  time (now `0.2.4`), PyPI tracking the monorepo version, and the
  standalone file set as a strict subset. Do not add a competing
  publisher here.
- Canonical release path (monorepo `.github/workflows/release.yml`):
  tags are the only trigger with scheme `<distribution>-v<version>`
  (for example `spikeforge-targets-v0.2.4`); one job parses the tag
  into distribution/version/package directory, then the publish job
  selects the matching per-distribution PyPI environment and mints
  a short-lived OIDC token (`id-token: write`, no stored API token).
- The release job refuses the tag unless three sources agree: the
  tag version equals the distribution `pyproject.toml` version, and
  `compatibility.json` lists that version in its latest release row.
  It also runs the packaging guards script before publishing.

## 3. Version authority: `compatibility.json` and the core pin

- Authority for cross-distribution versions is the monorepo
  `compatibility.json` `releases` table. Latest row at time of
  writing: `spikeforge 0.6.3`, `spikeforge-server 0.5.2`,
  `spikeforge-serve 0.2.7`, `spikeforge-clients 0.1.2`,
  `spikeforge-targets 0.2.4`, `spikeforge-io 0.1.7`,
  `spikeforge-hub 0.5.2`, `dashboard 0.3.0`.
- Core-pin rule enforced by the release job: every non-core
  distribution except declared core-free distributions (currently
  only `spikeforge-clients`) must pin core exactly as
  `spikeforge~=<matrix core version>`. A core-free distribution must
  declare no core dependency at all.
- This checkout tracks that rule. Current pin here:

  `spikeforge~=0.6.3` in `pyproject.toml` and in
  `.github/workflows/ci.yml` (with the public monorepo fallback
  `git+https://github.com/Capsize-Games/spikeforge.git@main`
  `#subdirectory=packages/spikeforge`, which needs no credentials).
- How to bump deliberately: read the latest `compatibility.json`
  row in `Capsize-Games/spikeforge`, update the pin in both files
  above to `spikeforge~=<matrix core>`, and update the comment that
  names the matrix core version. Never bump one file without the
  other; `tests/test_release_policy.py` guards their agreement.
  Version bumps of this distribution itself (`0.1.0` here versus
  `0.2.4` canonical) belong to the release phase, not to a pin fix.

## 4. Supported stack

- Python: `requires-python >=3.10`; CI runs the `3.10–3.13` matrix
  on GitHub-hosted Ubuntu workers. Core itself now requires
  `>=3.11`; this distribution keeps the `>=3.10` floor and relies on
  CI to prove the matrix.
- Torch: `torch>=2.5` with CPU wheels in CI (`TORCH_INDEX_URL`
  `https://download.pytorch.org/whl/cpu`). CI installs matching
  CPU `torch`/`torchvision` first so the later `spikeforge`
  resolution does not pull an ABI-incompatible CUDA build.
- Lint: `ruff check .` under `ruff.toml` (line-length 79,
  `py38` target, `A/ANN/B/C4/D/E/F/I/N/RET/SIM/UP/W`).
- Tests: `pytest`; dev extra pins `pytest>=7.0`,
  `pytest-cov>=4.0`, `ruff>=0.0.280`.

## 5. Compatibility matrix (targets)

Built-in specs live in `spikeforge_targets/catalog.py`; the
authoritative consumer view is `spikeforge_targets.capability_matrix`
(`classify`/`compare_targets`, JSON-serialisable rows per target):

- `reference` — always available, supports every emitted primitive.
- `norse` (extra `norse`) — PyTorch simulator; no `CubaLIF`,
  `Delay`, or `IF` (`IF` substitutes to `LIF`).
- `lava_loihi2` (extra `lava`) — Loihi 2 path; no native
  `AvgPool2d` (substitutes `SumPool2d` plus `Scale`), no `CubaLIF`
  or `IF`; defaults to the CPU emulator unless a device run is
  explicitly opted in.
- `spinnaker2` (extra `spinnaker2`) — no third-order neuron.
- `speck` (extra `speck`) — one conv/LIF chain, no pooling.
- `xylo` (extra `xylo`) — low-power LIF fabric, no conv/pooling.

Optional targets report unavailable while their SDK is absent
(`tests/test_target_registry.py` pins this); never claim a hardware
backend result from the CPU-only baseline.

## 6. Downstream consumers

- `999` (`Projects/999`) pins `spikeforge` and
  `spikeforge-targets` to a specific commit with a deliberate-bump
  comment rather than a live checkout. Bumping the family pin here
  does not obligate `999`; its bump is a separate deliberate step.
- `spikeforge-hub` follows the same core-pin rule from its own
  `pyproject.toml`; coordinate hub/targets bumps through the same
  `compatibility.json` row.

## 7. Scope guard

Documentation and pin convergence only. No code extraction, no
re-sync automation, no README redirect, no archive, and no new
publisher are authorized by this record. Backend file drift noted in
`docs/fleet-audit.md` (for example `backends/api.py` module maps)
remains outside this policy fix.
