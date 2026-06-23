---
name: beautiful-repo
description: Standardize deep learning and machine learning research repositories into reproducible, citation-ready, maintainable project structures and polished open-source releases. Use when auditing or refactoring PyTorch, TensorFlow, JAX, Lightning, Hugging Face, MONAI, or custom training repositories for project layout, experiment configuration, training/evaluation/inference entry points, Python code style, docstrings, naming, module boundaries, packaging, tests, documentation, beautiful README design, model cards, data cards, CITATION.cff, CI quality gates, and open-source research release readiness.
---

# Beautiful Repo

Use this skill to turn a deep learning repository into a reproducible, readable, citation-ready research artifact without breaking existing experiments.

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
- Implementation mode: make scoped edits, preserve compatibility, add tests/docs, and validate with smoke checks.
- README mode: improve the visual GitHub README, images, badges, quickstart, results, checkpoints, citation, and link hub.
- Code style mode: improve directory/file/API naming, docstrings, function boundaries, imports, type hints, and side-effect boundaries.
- Release mode: add or improve `CITATION.cff`, model cards, data cards, license notes, result tables, checkpoint instructions, and CI.
- Multi-agent mode: after an audit or code review, split implementation into focused agents for naming/code style, docstrings, README/docs, tests/CI, and release metadata when the environment supports subagents.

When the user asks for "everything" or "standardize the repo", cover README, docs, structure, naming, docstrings, configs, entry points, tests, CI, packaging, release metadata, artifacts, and compatibility. Do not stop after only README or only code style.

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
- Treat style work as user-facing engineering work. Improve names, docstrings, function boundaries, type hints, README presentation, and error messages only when it improves maintainability or reproducibility.
- Keep top-of-file module docstrings and function docstrings concise. Prefer short contract text over long explanations; move tutorials, derivations, and background to docs.
- Do not make cosmetic edits that obscure experiment logic, historical results, or paper reproduction commands.

## Review-To-Implementation Workflow

After an audit or review, use a multi-agent workflow when the environment supports it and the change is large enough to benefit from parallel review:

1. Produce a primary audit listing gaps and affected files.
2. Assign focused agents or passes:
   - Naming/code agent: directories, Python files, public APIs, module boundaries, imports, and side effects.
   - Docstring agent: concise module/function/class docstrings with tensor/config/checkpoint contracts.
   - README/docs agent: visual README, quickstart, data/reproduction/results docs, model/data cards.
   - Tests/CI agent: smoke tests, import/config/model-forward checks, lint/format/CI gates.
   - Release agent: citation, license, checkpoint tables, limitations, artifact hygiene.
3. Keep each agent's edits scoped and compatibility-preserving.
4. Run a final integrator pass to resolve conflicts, remove duplication, and verify that all coverage checklist areas were addressed or explicitly deferred.
5. Finish with validation commands, compatibility notes, and remaining risks.

If subagents are not available, simulate the same workflow as sequential passes with separate diffs or commits.

## First Pass

1. Inspect repository shape: root files, source directories, scripts, notebooks, configs, tests, data/checkpoint artifacts, CI, and docs.
2. Identify the repository type:
   - paper release: primary goal is reproducing figures/tables from a paper.
   - method library: reusable model, loss, trainer, or dataset code.
   - model zoo: many configs/checkpoints with common training/eval code.
   - application demo: inference-first with pretrained weights.
   - production ML: serving, monitoring, and deployment are primary concerns.
   - restricted scientific/medical release: data access, privacy, and protocol clarity are primary concerns.
3. Run `scripts/audit_dl_repo.py <repo>` from this skill when Python is available. Use the output as a checklist, not as an absolute verdict.
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
- Documentation: visual README, install, quickstart, data prep, training, evaluation, inference, results, checkpoints, troubleshooting, citation, license, acknowledgements.
- Release metadata: `CITATION.cff`, BibTeX, model card, data card, limitations, ethical/safety notes when relevant.
- Quality gates: import tests, config tests, model forward tests, dataset smoke tests, metric sanity tests, lint/format/type checks, CI.
- Artifact hygiene: `.gitignore`, large files, generated outputs, logs, cached datasets, checkpoints, and reproducible download instructions.
- Compatibility: old commands, old import paths, published config names, checkpoint names, README links, notebooks, CI commands, and paper reproduction commands.

## Target Repository Shape

Adapt names to the existing project, but converge toward this shape:

```text
repo/
  README.md
  LICENSE
  CITATION.cff
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
  docs/
    setup.md
    data.md
    reproduction.md
    results.md
    model_card.md
  examples/
    quickstart.ipynb
  assets/
    figures/
```

Keep large or generated paths out of git: `data/`, `datasets/`, `checkpoints/`, `weights/`, `runs/`, `wandb/`, `mlruns/`, `outputs/`, `logs/`, `lightning_logs/`, and `__pycache__/`.

## Migration Order

1. Establish safety: check git status, identify untracked artifacts, find current runnable commands, and record baseline import/test behavior.
2. Add repository hygiene: `.gitignore`, `pyproject.toml` tool config, pre-commit config, and minimal quality commands.
3. Add documentation scaffolding: README quickstart, environment setup, data preparation, reproduction, results, citation, and license notes.
4. Introduce stable entry points: `scripts/train.py`, `scripts/eval.py`, `scripts/infer.py`; keep wrappers around old commands when needed.
5. Centralize configuration: move hard-coded hyperparameters and paths into `configs/` only after entry points are stable.
6. Modularize code: separate data, models, losses, metrics, training loop, evaluation, inference, and utilities.
7. Normalize code style: apply project-local formatting, normalize directory/file/API names, add or improve public module/class/function docstrings, improve vague names, split oversized functions, and convert import-time side effects into explicit calls.
8. Add tests: start with import, config load, model forward, metric sanity, and dataset smoke tests using tiny synthetic data where possible.
9. Polish README and docs: make the repository useful within the first screen, then add full reproduction and result details.
10. Add CI: run lint, format check, tests, and import checks. Avoid GPU-only CI unless the repository already has GPU runners.
11. Add release metadata: `CITATION.cff`, model card, data card, checkpoint download instructions, BibTeX, and reproducibility notes.

## Minimum Done Criteria

A normalized deep learning repo should have:

- One documented environment creation path.
- One documented tiny smoke run that finishes quickly on CPU or explicitly states GPU requirements.
- One documented command to train, evaluate, and run inference.
- Config files for all published or representative experiments.
- Clear dataset acquisition/preparation instructions, including expected directory layout.
- Clear checkpoint/weight download instructions and checksum/version notes when available.
- Tests that prove imports, config loading, model construction, one forward pass, and at least one metric path.
- README sections for badges, visual project signal, installation, quickstart, reproduction, results, model/checkpoint table, citation, license, and acknowledgements.
- README images and links point to real assets or are explicitly removed. Do not leave `href="#"`, fake checkpoint links, fake metrics, or placeholder screenshots in a finished README.
- Directories, Python files, packages, public APIs, configs, experiments, CLI flags, and output paths follow a consistent naming convention or preserve a documented legacy convention.
- Public modules, classes, and functions use consistent naming, type hints where practical, and concise docstrings that explain ownership, tensor shapes, units, devices, configs, checkpoints, and side effects.
- Training, evaluation, and inference code avoids hidden import-time side effects, author-local absolute paths, and unstructured global state.
- `CITATION.cff` and BibTeX for paper repositories.
- `.gitignore` protecting large data, model weights, logs, and generated outputs.

## Output Style

When auditing, report:

1. Current repository classification.
2. High-impact gaps ordered by reproducibility risk.
3. Proposed target structure.
4. A phased migration plan with small reviewable steps.
5. Coverage status for structure, naming, code style, docs, tests, CI, release metadata, artifacts, and compatibility.
6. Commands used for validation and their results.

When editing, finish with changed files, preserved compatibility notes, and validation performed. If a full training run was not performed, say so explicitly.
