# Standardize DL Repo

Codex skill for standardizing deep learning and machine learning research repositories into reproducible, citation-ready, maintainable project structures.

Use it when you want an agent to audit or refactor PyTorch, TensorFlow, JAX, Lightning, Hugging Face, MONAI, or custom training repositories for:

- research-grade project layout
- train/eval/infer entry points
- experiment configuration
- reproducibility documentation
- smoke tests and quality gates
- model cards, data cards, and `CITATION.cff`
- GitHub-ready open-source release hygiene

## Install

Install the skill from this repository:

```bash
npx skills add <owner>/<repo> --skill standardize-dl-repo
```

Or install from a local checkout by copying the skill folder into your Codex skills directory:

```text
skills/standardize-dl-repo -> ~/.codex/skills/standardize-dl-repo
```

Restart Codex after installation.

## Use

Ask Codex:

```text
Use $standardize-dl-repo to audit this deep learning repository and propose a migration plan.
```

For an implementation pass:

```text
Use $standardize-dl-repo to normalize this PyTorch repository. Keep old training commands compatible, add missing docs/tests/configs, and validate with smoke checks.
```

## Repository Layout

```text
.
  skills/
    standardize-dl-repo/
      SKILL.md
      agents/
        openai.yaml
      references/
        framework-notes.md
        migration-playbook.md
        research-release-standard.md
      scripts/
        audit_dl_repo.py
  .github/
    workflows/
      validate.yml
```

## What The Skill Optimizes For

The skill is intentionally conservative. It tells Codex to preserve existing behavior, avoid full training runs unless requested, and migrate a repository in small reviewable steps.

It is most useful for research repositories where the expected output is not just clean code, but a reproducible artifact that another researcher can install, run, evaluate, and cite.

## Audit Script

The bundled audit script can be run directly:

```bash
python skills/standardize-dl-repo/scripts/audit_dl_repo.py /path/to/deep-learning-repo
```

The script checks for common release-readiness signals such as README, license, citation metadata, configs, entry points, tests, docs, CI, and artifact ignore rules.

The output is a starting checklist, not a substitute for reading the repository.

## License

MIT
