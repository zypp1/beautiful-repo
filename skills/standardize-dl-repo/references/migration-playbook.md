# Migration Playbook

Use this reference before changing layout or entry points in an existing deep learning repository.

## Step 0: Inventory

Collect:

- `git status --short`
- root files and top-level directories
- Python files and notebooks
- dependency files
- training/evaluation/inference commands from README, scripts, notebooks, and shell files
- large tracked or untracked artifacts
- current tests and CI

Do not move files until the current command surface is understood.

## Step 1: Compatibility Map

Create a table:

| Current path or command | Role | Keep, wrap, move, or deprecate |
| --- | --- | --- |
| `train.py` | training entry | wrap into `scripts/train.py` |

When moving a user-facing command, leave a small wrapper or update docs and mention the breaking change.

## Step 2: Add Hygiene Without Moving Code

Low-risk first changes:

- `.gitignore` for artifacts.
- `pyproject.toml` with `ruff`, `pytest`, and build metadata if packageable.
- `.pre-commit-config.yaml` when the project has or accepts pre-commit.
- `tests/test_imports.py`.
- README quickstart corrections.

## Step 3: Introduce `src/` Gradually

If code currently lives at root, move only after imports are understood.

Preferred flow:

1. Identify importable package name.
2. Create `src/<package>/`.
3. Move modules by responsibility, preserving relative imports.
4. Add compatibility imports or wrappers only when external users may import old paths.
5. Run import and smoke tests after each group.

Avoid broad import rewrites by hand when many files are involved; use an AST-aware or search-and-replace plan and verify with tests.

## Step 4: Normalize Entrypoints

Entrypoints should be thin:

- parse CLI args
- load config
- call package functions
- return process status

Training logic belongs under `src/<package>/training/`, not in `scripts/train.py`.

Add `--config`, `--data-root`, `--output-dir`, `--seed`, `--device`, and `--dry-run` where reasonable.

## Step 5: Normalize Configs

Move hard-coded values into configs only after tests or smoke commands exist.

Required config practices:

- no author-local absolute paths
- output directory configurable
- seed configurable
- dataset root configurable
- published experiment configs named clearly
- defaults documented in README or `docs/reproduction.md`

## Step 6: Validate

Run the cheapest meaningful checks:

- format/lint check
- package import
- config load
- CLI `--help`
- model forward on tiny input
- dataset smoke with tiny fixture or clear missing-data error

For GPU projects, add CPU smoke tests where possible and document GPU-only paths separately.

## Step 7: Document The New Contract

Update:

- README quickstart
- `docs/setup.md`
- `docs/data.md`
- `docs/reproduction.md`
- `docs/results.md`
- `CITATION.cff`

State old command compatibility or migration notes when applicable.
