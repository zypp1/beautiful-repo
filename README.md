<div align="center">
  <h1>Beautiful DL Repo</h1>
  <p><strong>Codex skill for turning deep learning repositories into beautiful, reproducible, citation-ready research releases.</strong></p>
  <p>
    <a href="skills/beautiful-dl-repo/SKILL.md"><img src="https://img.shields.io/badge/Codex%20Skill-beautiful--dl--repo-111827" alt="Codex Skill"></a>
    <a href="skills/beautiful-dl-repo/references/readme-standard.md"><img src="https://img.shields.io/badge/README-visual%20standard-2563eb" alt="README visual standard"></a>
    <a href="#license"><img src="https://img.shields.io/badge/License-MIT-16a34a" alt="License"></a>
  </p>
  <p>
    <a href="skills/beautiful-dl-repo/SKILL.md">Skill</a> |
    <a href="skills/beautiful-dl-repo/references/readme-standard.md">README Standard</a> |
    <a href="skills/beautiful-dl-repo/references/code-style-standard.md">Code Style</a> |
    <a href="skills/beautiful-dl-repo/assets/readme-templates/visual-research-readme.md">Visual Template</a> |
    <a href="skills/beautiful-dl-repo/scripts/audit_dl_repo.py">Audit Script</a>
  </p>
</div>

<table>
  <tr>
    <td><strong>README polish</strong><br>Hero, badges, link hub, cards, gallery, quickstart, checkpoints, and results.</td>
    <td><strong>Research release</strong><br>Configs, reproduction docs, model/data cards, citation, license, and limitations.</td>
    <td><strong>Python quality</strong><br>Docstrings, tensor contracts, names, module boundaries, tests, and CI gates.</td>
  </tr>
</table>

Use it when you want an agent to audit or refactor PyTorch, TensorFlow, JAX, Lightning, Hugging Face, MONAI, or custom training repositories for:

- research-grade project layout
- train/eval/infer entry points
- Python code style, names, docstrings, and module boundaries
- experiment configuration
- reproducibility documentation
- polished README design
- smoke tests and quality gates
- model cards, data cards, and `CITATION.cff`
- GitHub-ready open-source release hygiene

## Install

Install the skill with any Codex-compatible skills installer that supports GitHub repositories:

```bash
npx skills add <owner>/<repo> --skill beautiful-dl-repo
```

If your installer uses a different command, point it at `skills/beautiful-dl-repo`.

For a local checkout, copy the skill folder into your Codex skills directory:

```text
skills/beautiful-dl-repo -> ~/.codex/skills/beautiful-dl-repo
```

Restart Codex after installation.

## Use

Ask Codex:

```text
Use $beautiful-dl-repo to audit this deep learning repository and propose a migration plan.
```

For an implementation pass:

```text
Use $beautiful-dl-repo to normalize this PyTorch repository. Keep old training commands compatible, add missing docs/tests/configs, polish the visual README, and validate with smoke checks.
```

## Repository Layout

```text
.
  skills/
    beautiful-dl-repo/
      SKILL.md
      agents/
        openai.yaml
      references/
        code-style-standard.md
        framework-notes.md
        high-impact-patterns.md
        migration-playbook.md
        readme-standard.md
        repo-type-playbooks.md
        research-release-standard.md
        sources-reviewed.md
      scripts/
        audit_dl_repo.py
      assets/
        readme-templates/
          visual-research-readme.md
  tests/
    test_audit_dl_repo.py
  .github/
    workflows/
      validate.yml
```

## What The Skill Optimizes For

The skill is intentionally conservative. It tells Codex to preserve existing behavior, avoid full training runs unless requested, and migrate a repository in small reviewable steps.

It is most useful for research repositories where the expected output is not just clean code, but a reproducible artifact that another researcher can install, run, evaluate, and cite.

The standards were distilled from a representative sample of high-impact deep learning repositories and official project hygiene references, including Transformers, Diffusers, MMDetection, Detectron2, Segment Anything, timm, Ultralytics, nnU-Net, MONAI, PyTorch Lightning, TorchVision, CLIP, PEP 8, PEP 257, GitHub README/CITATION guidance, Ruff, pytest, and Python packaging guidance.

The full source list is in `skills/beautiful-dl-repo/references/sources-reviewed.md`.

## Audit Script

The bundled audit script can be run directly:

```bash
python skills/beautiful-dl-repo/scripts/audit_dl_repo.py /path/to/deep-learning-repo
```

The script checks for common release-readiness signals such as README, license, citation metadata, configs, entry points, tests, docs, CI, and artifact ignore rules.

The output is a starting checklist, not a substitute for reading the repository.

## License

MIT
