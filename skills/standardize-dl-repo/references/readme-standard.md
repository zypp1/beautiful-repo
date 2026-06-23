# README Standard

Use this reference before writing or polishing a deep learning repository README.

## First Screen

The first visible screen should answer:

- What is this?
- What task does it solve?
- Where are the paper, project page, docs, demo, and checkpoints?
- What does the model output look like?
- How do I install and run one minimal command?

Recommended order:

```markdown
# Project Name

One-sentence task/model/research claim.

[Paper] [Project Page] [Demo] [Docs] [Checkpoints] [Dataset] [Citation]

![Representative output](assets/figures/teaser.png)

## Quickstart
```

Use badges sparingly. Good badges: license, tests, docs, package version, paper/arXiv, model hub. Avoid noisy badges that do not help users decide whether to use the repo.

## Required Sections

Use the sections that fit the project:

- Overview
- News or Updates
- Installation
- Quickstart
- Data Preparation
- Pretrained Models / Checkpoints
- Training
- Evaluation
- Inference / Demo
- Reproducing Paper Results
- Results
- Configuration
- Repository Structure
- Model Card / Limitations
- Citation
- License
- Acknowledgements

For a small paper repo, keep the README complete but not encyclopedic; move long setup, data, reproduction, and results details into `docs/`.

## Quickstart Quality Bar

A good quickstart:

- starts from a fresh clone
- states Python/CUDA/framework version expectations
- installs dependencies in one command or short block
- downloads or references a tiny sample/checkpoint
- runs inference or a smoke test
- writes outputs to a documented directory

Example:

```bash
python -m pip install -e ".[dev]"
python scripts/infer.py \
  --config configs/demo.yaml \
  --checkpoint checkpoints/demo.pt \
  --input assets/examples/image.jpg \
  --output outputs/demo
```

## Checkpoint Table

Use tables when there are multiple models:

| Model | Config | Dataset | Metric | Checkpoint | Notes |
| --- | --- | --- | --- | --- | --- |
| `model_name` | `configs/experiments/model.yaml` | Dataset v1 | 88.1 mIoU | link | paper setting |

Include file size and checksum when practical.

## Results Table

Results should be auditable:

| Setting | Dataset split | Checkpoint | Command | Metric | Expected |
| --- | --- | --- | --- | --- | --- |
| Paper main | test | `model.pt` | `python scripts/eval.py ...` | mAP | 42.0 |

State tolerance and known nondeterminism.

## Visual Presentation

- Use one clear teaser, architecture diagram, or qualitative result near the top.
- Keep images committed under `assets/figures/` when small; use external hosting or releases for large files.
- Prefer short paragraphs, tables, and command blocks.
- Keep heading levels consistent.
- Avoid walls of badges, huge GIFs, uncompressed images, and long changelogs above usage instructions.

## Citation Section

Include both `CITATION.cff` and BibTeX when there is a paper:

```markdown
## Citation

If this repository helps your research, please cite:

```bibtex
@inproceedings{...}
```
```

Make sure citation title/authors/year match the paper and `CITATION.cff`.

## Honest Limitations

Add a short limitations section for pretrained models:

- intended use
- unsupported use
- dataset bias or domain constraints
- hardware/runtime constraints
- expected failure cases

For medical, human-subject, biometric, or safety-sensitive repositories, link to a model card or data card.
