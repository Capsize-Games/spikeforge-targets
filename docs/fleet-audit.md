# Fleet audit — spikeforge-targets

Fleet-audit record for
[Capsize-Games/spikeforge-targets#3](https://github.com/Capsize-Games/spikeforge-targets/issues/3).
Docs only. Verified against `main` on 2026-10-13
(`pyproject.toml` version `0.1.0`) and against `origin/main` of
`Capsize-Games/spikeforge` and PyPI on the same day.

## 1. Identity, boundary, owner, runtime

- **Canonical identity.** GitHub `Capsize-Games/spikeforge-targets`
  (public, default branch `main`); local checkout
  `Projects/spikeforge/spikeforge-targets`.
- **Owner and license.** Capsize LLC (`contact@capsizegames.com`),
  BSD-3-Clause. Public history; no rewrite or deletion is
  authorized by this audit.
- **Product boundary.** This repository owns the
  `spikeforge_targets` import root: deployment-target adapters,
  event-driven energy accounting, quantization, and the optional
  Norse/Lava backend integrations. Dependency direction is
  targets-to-core; the `spikeforge` core package never depends on
  this package. Backend SDKs stay optional extras with explicit
  skip/availability behavior; the CPU-only baseline is the
  supported default.
- **Supported runtimes.** Python `>=3.10`; CI runs the 3.10–3.13
  matrix on GitHub-hosted Ubuntu workers with CPU torch wheels.
- **Deployment channel: none from this repository.** The only
  workflow is `ci.yml`; there is no release workflow and no PyPI
  trusted publisher here. PyPI `spikeforge-targets` publishes from
  the monorepo (section 3).
- **Migration metadata.** `capsize.json` and `justfile` are present
  (`setup`/`build`/`test`/`lint`/`ci`); the local task contract in
  `AGENTS.md` matches them.

## 2. Dependency table (`pyproject.toml` @ 0.1.0)

| Dependency | Current here | Canonical (monorepo `packages/spikeforge-targets` @ 0.2.1) | Proposed authority |
| --- | --- | --- | --- |
| `spikeforge` | `~=0.3.0` | `~=0.5.2` | Monorepo; this pin is two minor lines stale |
| `numpy` | `>=1.26` | `>=1.26` | Agreed; no change |
| `torch` | `>=2.5` | `>=2.5` | Agreed; no change |
| `dev` (`pytest`, `pytest-cov`, `ruff`) | pinned floors | pinned floors | Agreed; no change |
| `norse` extra | `norse` | `norse` | Agreed; stays optional |
| `lava` extra | `lava-nc` | `lava-nc` | Agreed; stays optional |

Backend/framework dependencies stay explicit and targets-local in
both copies. The canonical copy additionally recognizes `speck`
(`sinabs`), `xylo` (`rockpool`), and `spinnaker2` backends in
`backends/api.py` with capability probing; those mappings live only
in the monorepo, so the compatibility matrix's authority is the
monorepo copy. Nothing here is a candidate for `capsize-commons`
or any frontend package, and optional accelerator dependencies
must not move into either.

## 3. Monorepo-canonical evidence

PyPI `spikeforge-targets` builds from monorepo
`packages/spikeforge-targets`, and this standalone repository is a
stale mirror of that source. Evidence, each item verified directly:

1. **Version lineage.** Standalone `main`: `0.1.0`. Monorepo
   `packages/spikeforge-targets/pyproject.toml` on `origin/main`:
   `0.2.1`. PyPI `spikeforge-targets` latest: `0.2.1`. The PyPI
   version equals the monorepo version, not the standalone one.
2. **Release path.** Monorepo `.github/workflows/release.yml`
   publishes `packages/<distribution>` to PyPI from
   `<distribution>-v<version>` tags via a per-distribution trusted
   publisher. This repository has no corresponding workflow.
3. **File counts.** Standalone `spikeforge_targets/`: **57**
   files. Monorepo `spikeforge_targets/`: **68** files. Files
   present only in the standalone: **none** — it is a strict
   subset.
4. **Monorepo-only files (11).** `activation_quant.py`,
   `activation_quant_graph.py`, `activation_quant_keys.py`,
   `activation_quant_records.py`, `activation_quant_report.py`,
   `backends/vendor_backend.py`, `cli/deploy_cli.py`,
   `fixed_point.py`, `py.typed`, `test_deploy.py`, and
   `test_deploy_result.py`.
5. **Shared-file drift.** 23 of the 57 shared files differ
   byte-for-byte. Example, `backends/api.py`: the monorepo copy
   adds the `speck`/`xylo`/`spinnaker2` backend mappings, a
   `BACKEND_CAPABILITIES` table with `module_with_capability`
   probing (an installed-but-unrecognized SDK reports unavailable
   rather than trusted), and a `torch` import; the standalone copy
   maps only `norse` and `lava_loihi2`.
6. **Packaging drift.** Core pin `~=0.3.0` versus `~=0.5.2`.

## 4. Keep / migrate / retire and scope-guard close

- **Keep:** the package-boundary definition (targets own adapters
  and energy accounting; core never depends on targets), the
  optional-backend gating with explicit skip behavior, the
  CPU-only baseline, and the `capsize.json`/`justfile` task
  contract.
- **Migrate:** none. Every shared-code candidate in this
  repository already exists in a newer form at the canonical
  monorepo path, so there is no extraction with a consumer, API
  shape, and compatibility test to propose. A monorepo-to-mirror
  re-sync would run in the opposite direction and is out of scope
  here.
- **Retire:** none in this PR. This audit deletes nothing.

Per the issue's scope guard, the migration portion is **closed with
this evidence**: no extraction from this repository is warranted.
The mirror's own disposition (re-sync automation, README redirect,
or archive) is a follow-up decision left to the fleet coordinator;
this record authorizes none of those outcomes by itself.
