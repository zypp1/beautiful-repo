---
name: standardize-dl-repo
description: Standardize deep learning and machine learning research repositories into reproducible, citation-ready, maintainable project structures. Use when auditing or refactoring PyTorch, TensorFlow, JAX, Lightning, Hugging Face, MONAI, or custom training repositories for project layout, experiment configuration, training/evaluation/inference entry points, packaging, tests, documentation, model cards, data cards, CITATION.cff, CI quality gates, and open-source research release readiness.
---

# Standardize DL Repo

Use this skill to turn a deep learning repository into a reproducible research artifact without breaking existing experiments.

## Operating Rules

- Preserve existing behavior first. Treat every move, rename, and configuration change as a migration that must keep old commands working or document the replacement.
- Do not delete datasets, checkpoints, generated outputs, logs, or experiment artifacts. Add ignore rules and relocation guidance instead.
- Do not run full training unless the user explicitly asks. Prefer import checks, config parsing, dataset smoke tests, one-batch tests, and model forward tests.
- Separate mechanical cleanup from behavioral changes. Keep formatting, layout migration, dependency changes, and training logic changes independently reviewable.
- Prefer the repository's current framework and conventions. Do not introduce Hydra, Lightning, uv, DVC, MLflow, or Weights & Biases unless the project already uses them or the user approves.
- Keep notebooks as examples or analysis artifacts, not as the only training/evaluation path.

## First Pass

1. Inspect repository shape: root files, source directories, scripts, notebooks, configs, tests, data/checkpoint artifacts, CI, and docs.
2. Identify the repository type:
   - paper release: primary goal is reproducing figures/tables from a paper.
   - method library: reusable model, loss, trainer, or dataset code.
   - model zoo: many configs/checkpoints with common training/eval code.
   - application demo: inference-first with pretrained weights.
   - production ML: serving, monitoring, and deployment are primary concerns.
3. Run `scripts/audit_dl_repo.py <repo>` from this skill when Python is available. Use the output as a checklist, not as an absolute verdict.
4. Read the relevant reference:
   - `references/research-release-standard.md` for paper/research repositories.
   - `references/migration-playbook.md` before moving files or changing entry points.
   - `references/framework-notes.md` when framework-specific choices matter.

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
7. Add tests: start with import, config load, model forward, metric sanity, and dataset smoke tests using tiny synthetic data where possible.
8. Add CI: run lint, format check, tests, and import checks. Avoid GPU-only CI unless the repository already has GPU runners.
9. Add release metadata: `CITATION.cff`, model card, data card, checkpoint download instructions, BibTeX, and reproducibility notes.

## Minimum Done Criteria

A normalized deep learning repo should have:

- One documented environment creation path.
- One documented tiny smoke run that finishes quickly on CPU or explicitly states GPU requirements.
- One documented command to train, evaluate, and run inference.
- Config files for all published or representative experiments.
- Clear dataset acquisition/preparation instructions, including expected directory layout.
- Clear checkpoint/weight download instructions and checksum/version notes when available.
- Tests that prove imports, config loading, model construction, one forward pass, and at least one metric path.
- README sections for installation, quickstart, reproduction, results, citation, license, and acknowledgements.
- `CITATION.cff` and BibTeX for paper repositories.
- `.gitignore` protecting large data, model weights, logs, and generated outputs.

## Output Style

When auditing, report:

1. Current repository classification.
2. High-impact gaps ordered by reproducibility risk.
3. Proposed target structure.
4. A phased migration plan with small reviewable steps.
5. Commands used for validation and their results.

When editing, finish with changed files, preserved compatibility notes, and validation performed. If a full training run was not performed, say so explicitly.
