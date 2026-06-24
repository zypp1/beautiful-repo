---
name: beautiful-repo
description: Standardize deep learning and machine learning repositories by first profiling repository scale, framework, content, and release intent, then matching an appropriate high-impact GitHub structure. Use when auditing or refactoring PyTorch, TensorFlow, JAX, Lightning, Hugging Face, MONAI, model zoo, paper-code, demo, or custom training repositories for adaptive project layout, experiment configuration, training/evaluation/inference entry points, senior-engineer Python code style, concise docstrings, naming, module boundaries, packaging, tests, minimal README, real arXiv/Bilibili/demo/model/data/checkpoint links, CI quality gates, and optional research release readiness.
---

# Beautiful Repo

Use this skill to turn a deep learning repository into a reproducible, readable project without forcing every repo into the same template. Profile the repository first, then match the smallest high-impact structure that fits its scale and content.

## How To Use

Call the skill by name and state the mode:

```text
Use $beautiful-repo to audit this PyTorch repository. Do not edit files yet.
```

```text
Use $beautiful-repo to normalize this deep learning repository. Keep old train/eval commands compatible and make small reviewable commits.
```

```text
Use $beautiful-repo to improve naming, docstrings, module boundaries, and README polish for this repository.
```

Use these modes:

- Audit mode: inspect only, run the audit script when Python is available, classify the repo, and produce a prioritized migration plan.
- Implementation mode: make scoped edits, preserve compatibility, add tests and minimal README updates, and validate with smoke checks.
- README mode: improve the GitHub README with minimal quickstart and real links to arXiv, Bilibili/YouTube, demos, model hubs, datasets, checkpoints, and citation when they exist.
- Code style mode: improve directory/file/API naming, docstrings, function boundaries, imports, type hints, and side-effect boundaries.
- Release mode: add or improve `CITATION.cff`, model cards, data cards, license notes, result tables, checkpoint instructions, and CI.
- Multi-agent mode: after an audit or code review, split implementation into focused agents for naming/code style, docstrings, README quickstart, tests/CI, and optional release metadata when the environment supports subagents.

When the user asks for "everything" or "standardize the repo", prioritize repository profiling, adaptive structure, naming, code style, configs, entry points, tests, CI, packaging, artifact hygiene, compatibility, and a minimal useful README. Treat full docs, model cards, data cards, `CITATION.cff`, and long release notes as optional unless the repository is a paper/model release or the user explicitly asks.

## Beautiful Means

Optimize for these outcomes, in order:

- Beautiful to understand in 60 seconds: the first screen shows the task, model family, output, links, and main result without requiring a paper read.
- Beautiful to run in 5 minutes: a fresh clone has one install path and one tiny CPU or clearly GPU-marked smoke command.
- Beautiful to reproduce: configs, checkpoints, data layout, evaluation commands, metrics, and expected tolerance are connected.
- Beautiful to inspect visually: README images are real outputs, architecture diagrams, screenshots, or synthetic-safe examples, not decorative filler.
- Beautiful to extend: Python modules have clear boundaries, names, docstrings, tensor contracts, and explicit side effects.
- Beautiful to cite: paper, BibTeX, `CITATION.cff`, license, model/data limitations, and acknowledgements are discoverable.

## Operating Rules

- Preserve existing behavior first. Treat every move, rename, and configuration change as a migration that must keep old commands working or document the replacement.
- Do not delete datasets, checkpoints, generated outputs, logs, or experiment artifacts. Add ignore rules and relocation guidance instead.
- Do not run full training unless the user explicitly asks. Prefer import checks, config parsing, dataset smoke tests, one-batch tests, and model forward tests.
- Separate mechanical cleanup from behavioral changes. Keep formatting, layout migration, dependency changes, and training logic changes independently reviewable.
- Prefer the repository's current framework and conventions. Do not introduce Hydra, Lightning, uv, DVC, MLflow, or Weights & Biases unless the project already uses them or the user approves.
- Keep notebooks as examples or analysis artifacts, not as the only training/evaluation path.
- Lower documentation priority for normal repositories. Add only README sections needed to install, run, evaluate, and understand results. Do not create `docs/`, model cards, data cards, `CITATION.cff`, or long documentation unless the repo type or user request justifies them.
- Do not use local docs links as README filler. The README link hub is for real external resources such as arXiv, OpenReview, Bilibili, YouTube, project pages, Hugging Face, ModelScope, dataset pages, demos, checkpoints, and release assets. If those links do not exist, omit the slot.
- Treat style work as user-facing engineering work. Improve names, docstrings, function boundaries, type hints, README presentation, and error messages only when it improves maintainability or reproducibility.
- Keep top-of-file module docstrings and function docstrings concise. Prefer short contract text over long explanations; move tutorials, derivations, and background out of code.
- Do not make cosmetic edits that obscure experiment logic, historical results, or paper reproduction commands.

## Review-To-Implementation Workflow

After an audit or review, use a multi-agent workflow when the environment supports it and the change is large enough to benefit from parallel review:

1. Produce a primary audit listing repository scale, framework signals, repo type, recommended structure, gaps, and affected files.
2. Assign focused agents or passes:
   - Naming/code agent: directories, Python files, public APIs, module boundaries, imports, and side effects.
   - Docstring agent: concise module/function/class docstrings with tensor/config/checkpoint contracts.
   - README agent: minimal README quickstart by default; real arXiv/Bilibili/demo/model/data/checkpoint links when available; no local docs filler.
   - Tests/CI agent: smoke tests, import/config/model-forward checks, lint/format/CI gates.
   - Release agent: citation, license, checkpoint tables, limitations, artifact hygiene.
3. Keep each agent's edits scoped and compatibility-preserving.
4. Run a final integrator pass to resolve conflicts, remove duplication, and verify that all coverage checklist areas were addressed or explicitly deferred.
5. Finish with validation commands, compatibility notes, and remaining risks.

If subagents are not available, simulate the same workflow as sequential passes with separate diffs or commits.

## First Pass

1. Inspect repository shape and scale: file count, Python file count, framework imports, root files, source directories, scripts, notebooks, configs, tests, data/checkpoint artifacts, CI, and README signals.
2. Identify the repository type and size:
   - paper release: primary goal is reproducing figures/tables from a paper.
   - method library: reusable model, loss, trainer, or dataset code.
   - model zoo: many configs/checkpoints with common training/eval code.
   - application demo: inference-first with pretrained weights.
   - production ML: serving, monitoring, and deployment are primary concerns.
   - restricted scientific/medical release: data access, privacy, and protocol clarity are primary concerns.
3. Run `scripts/audit_dl_repo.py <repo>` from this skill when Python is available. Use its profile, framework signals, and recommended structure as the initial hypothesis, not as an absolute verdict.
4. Read the relevant reference:
   - `references/repo-type-playbooks.md` immediately after classifying the repository type.
   - `references/high-impact-patterns.md` before claiming or applying "high-quality deep learning repository" standards.
   - `references/research-release-standard.md` for paper/research repositories.
   - `references/migration-playbook.md` before moving files or changing entry points.
   - `references/code-style-standard.md` before editing Python code internals, names, type hints, or module boundaries.
   - `references/naming-standard.md` before renaming directories, files, public APIs, configs, experiments, CLI flags, or output paths.
   - `references/docstring-standard.md` before adding, auditing, or improving module/class/function docstrings.
   - `references/readme-standard.md` before writing or polishing README files.
   - `references/framework-notes.md` when framework-specific choices matter.

## Coverage Checklist

Always evaluate these areas before calling a repository normalized:

- Repository shape: root files, `src/` package layout, `scripts/`, `configs/`, `tests/`, `docs/`, `examples/`, `assets/`.
- Naming: directory names, Python file names, package names, public classes/functions, variables, constants, config names, experiment names, CLI flags, and output paths.
- Entry points: train, eval, inference, export, data/weight download, and CLI help paths.
- Configuration: defaults, experiment configs, path resolution, seeds, hardware assumptions, and reproducibility knobs.
- Code internals: module boundaries, function size, imports, typing, docstrings, error messages, side effects, and dependency boundaries.
- Deep learning contracts: tensor shapes, dtypes, devices, batch keys, metrics, checkpoints, randomness, distributed assumptions, and mixed precision behavior.
- Documentation: minimal README install, quickstart, data prep, train/eval/infer commands, results/checkpoints when relevant, and license. Full docs are optional for normal repositories.
- Release metadata: optional by default; add `CITATION.cff`, BibTeX, model card, data card, limitations, and ethical/safety notes for paper/model releases or explicit user requests.
- Quality gates: scale CI to the repository. Tiny/small repos should default to cheap push checks plus fuller PR/manual validation; larger libraries/model zoos can justify lint, format, import tests, config tests, model-forward tests, dataset smoke tests, and type checks in CI.
- Artifact hygiene: `.gitignore`, large files, generated outputs, logs, cached datasets, checkpoints, and reproducible download instructions.
- Compatibility: old commands, old import paths, published config names, checkpoint names, README links, notebooks, CI commands, and paper reproduction commands.

## Adaptive Target Shape

Do not force one layout onto every repository. Match the smallest structure that fits the repository profile:

- Tiny/small paper release: `README.md`, `LICENSE`, `pyproject.toml` or requirements, `configs/`, `scripts/`, optional `src/` only for reused code, `tests/`, assets for real figures.
- Small inference demo: `README.md`, `scripts/infer.py`, sample assets, checkpoint/model hub links, minimal tests, optional package only if code is reused.
- Medium research codebase: `src/<package>/`, `configs/experiments/`, `scripts/`, `tests/`, examples, minimal README, optional release metadata.
- Method/library: `src/<package>/`, API examples, tests, packaging metadata, concise public docstrings, compatibility notes.
- Model zoo/benchmark: config tree, tools/scripts, checkpoint/result tables, model index when the ecosystem uses one, CI and tests sized to the project.
- Production ML: package/service boundaries, deployment smoke tests, request/response examples, operational limits.

Use this general shape only after the profile justifies it:

```text
repo/
  README.md
  LICENSE
  pyproject.toml
  requirements.txt or uv.lock
  .gitignore
  .pre-commit-config.yaml
  .github/workflows/quality.yml
  configs/
    default.yaml
    experiments/
  src/
    project_name/
      __init__.py
      data/
      models/
      losses/
      metrics/
      training/
      evaluation/
      inference/
      utils/
  scripts/
    train.py
    eval.py
    infer.py
    export.py
  tests/
    test_imports.py
    test_model_forward.py
    test_dataset_smoke.py
  docs/                  # optional; only for substantial complex setup/reproduction/API material
  examples/
    quickstart.ipynb
  assets/
    figures/
```

Keep large or generated paths out of git: `data/`, `datasets/`, `checkpoints/`, `weights/`, `runs/`, `wandb/`, `mlruns/`, `outputs/`, `logs/`, `lightning_logs/`, and `__pycache__/`.

## Migration Order

1. Establish safety: check git status, identify untracked artifacts, find current runnable commands, and record baseline import/test behavior.
2. Add repository hygiene: `.gitignore`, `pyproject.toml` tool config, pre-commit config, and minimal quality commands.
3. Add minimal README scaffolding: environment setup, data preparation, quickstart, train/eval/infer commands, results/checkpoints when relevant, license notes, and real external links when available.
4. Introduce stable entry points: `scripts/train.py`, `scripts/eval.py`, `scripts/infer.py`; keep wrappers around old commands when needed.
5. Centralize configuration: move hard-coded hyperparameters and paths into `configs/` only after entry points are stable.
6. Modularize code: separate data, models, losses, metrics, training loop, evaluation, inference, and utilities.
7. Normalize code style: apply project-local formatting, normalize directory/file/API names, add or improve public module/class/function docstrings, improve vague names, split oversized functions, and convert import-time side effects into explicit calls.
8. Add tests: start with import, config load, model forward, metric sanity, and dataset smoke tests using tiny synthetic data where possible.
9. Polish README enough for use: first-screen purpose, install, quickstart, data, train/eval/infer, results/checkpoints when relevant. Add full docs only for paper/model releases or explicit user requests.
10. Add CI only at the weight the repo deserves. For tiny/small repos, push should run file/metadata checks and syntax/import smoke tests only; run full tests on pull requests or manual dispatch. Add lint, format, type checks, dataset/model smoke tests, and matrix jobs only when the repository size and user surface justify the cost. Avoid GPU-only CI unless the repository already has GPU runners.
11. Add release metadata only when relevant: `CITATION.cff`, model card, data card, checkpoint download instructions, BibTeX, and reproducibility notes for paper/model releases.

## Minimum Done Criteria

A normalized deep learning repo should have:

- One documented environment creation path.
- One documented tiny smoke run that finishes quickly on CPU or explicitly states GPU requirements.
- One documented command to train, evaluate, and run inference.
- Config files for all published or representative experiments.
- Clear dataset acquisition/preparation instructions, including expected directory layout.
- Clear checkpoint/weight download instructions and checksum/version notes when available.
- Tests that prove imports, config loading, model construction, one forward pass, and at least one metric path.
- CI, if added, is cheap on push and does not install heavyweight training dependencies for small repos unless the user explicitly wants that gate.
- README sections for purpose, installation, quickstart, data, train/eval/infer commands, results/checkpoints when relevant, and license.
- README images and links point to real assets or are explicitly removed. Do not leave `href="#"`, fake checkpoint links, fake metrics, or placeholder screenshots in a finished README.
- Directories, Python files, packages, public APIs, configs, experiments, CLI flags, and output paths follow a consistent naming convention or preserve a documented legacy convention.
- Public modules, classes, and functions use consistent naming, type hints where practical, and concise docstrings that explain ownership, tensor shapes, units, devices, configs, checkpoints, and side effects.
- Training, evaluation, and inference code avoids hidden import-time side effects, author-local absolute paths, and unstructured global state.
- `CITATION.cff` and BibTeX only for paper/model release repositories or explicit user requests.
- `.gitignore` protecting large data, model weights, logs, and generated outputs.

## Output Style

When auditing, report:

1. Current repository classification.
2. High-impact gaps ordered by reproducibility risk.
3. Proposed target structure.
4. A phased migration plan with small reviewable steps.
5. Coverage status for structure, naming, code style, minimal README, tests, CI, artifacts, and compatibility. Separately list optional docs/release metadata only when relevant.
6. Commands used for validation and their results.

When editing, finish with changed files, preserved compatibility notes, and validation performed. If a full training run was not performed, say so explicitly.
