# Contributing

Keep this repository focused on one job: helping Codex standardize deep learning research repositories.

## Guidelines

- Keep `skills/standardize-dl-repo/SKILL.md` concise and procedural.
- Put longer standards or framework-specific guidance in `references/`.
- Keep scripts deterministic and safe by default.
- When adding new standards, name the source repositories or official documents that motivated them.
- Do not add files that duplicate skill instructions without improving runtime behavior.
- Validate the skill metadata and Python script syntax before opening a pull request.

## Local Validation

```bash
python -m py_compile skills/standardize-dl-repo/scripts/audit_dl_repo.py
python skills/standardize-dl-repo/scripts/audit_dl_repo.py .
```
