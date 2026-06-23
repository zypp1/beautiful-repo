# README Standard

Use this reference before writing or polishing a deep learning repository README. The README should feel like a clear research product page: visual first, scannable cards second, full reproducibility details third.

For a ready-to-copy skeleton, use `assets/readme-templates/visual-research-readme.md`.

## First Screen

The first visible screen should answer:

- What is this?
- What task does it solve?
- Where are the paper, project page, docs, demo, and checkpoints?
- What does the model output look like?
- How do I install and run one minimal command?

Recommended order:

```markdown
<div align="center">

# Project Name

**One-sentence task/model/research claim.**

[Paper](#) | [Project Page](#) | [Demo](#) | [Docs](#) | [Checkpoints](#) | [Dataset](#) | [Citation](#)

![Representative output](assets/figures/teaser.png)

</div>

## Quickstart
```

Use badges sparingly. Good badges: license, tests, docs, package version, paper/arXiv, model hub. Avoid noisy badges that do not help users decide whether to use the repo.

## High-Star README Patterns

High-star repositories tend to converge on the same presentation structure:

- centered hero with title, short claim, badges, and compact link hub
- one strong image or GIF before long prose
- very short "install + run" path near the top
- feature cards or use-case cards for fast scanning
- example gallery for visual products or model outputs
- model/checkpoint/result tables for technical credibility
- deeper docs linked instead of copied into the README

For deep learning repositories, prefer this order:

1. Hero: logo/title, one-sentence claim, badges, link hub.
2. Visual proof: teaser image, demo GIF, qualitative grid, or architecture/result image.
3. At-a-glance cards: task, model, datasets, best metric, runtime, checkpoints.
4. Quickstart: install and one inference/demo command.
5. Model/result cards: pretrained models, benchmark results, reproduction commands.
6. Details: setup, data, training, evaluation, docs, citation, license.

## Visual README Requirements

For deep learning repositories, prefer a card-based README over a plain text-only README.

Minimum visual standard:

- one teaser image, qualitative result grid, architecture diagram, or demo GIF near the top
- one compact link hub for paper, project page, docs, demo, dataset, checkpoints, and citation
- one task/model information card block
- one results or benchmark card/table
- one checkpoint/model card table
- one quickstart command visible before long documentation

Use `assets/figures/teaser.png` or `assets/figures/overview.png` for primary visuals. If no real image exists, create a placeholder figure only if the user approves; do not invent qualitative results or fake metrics.

## Card Templates

GitHub README supports a safe subset of HTML. Use HTML tables for visually stable "cards" because they render reliably on GitHub.

### Hero With Link Hub

```markdown
<div align="center">
  <h1>Project Name</h1>
  <p><strong>Short model/task claim in one sentence.</strong></p>
  <p>
    <a href="#"><img src="https://img.shields.io/badge/Paper-arXiv-b31b1b" alt="Paper"></a>
    <a href="#"><img src="https://img.shields.io/badge/Docs-online-blue" alt="Docs"></a>
    <a href="#"><img src="https://img.shields.io/badge/License-MIT-green" alt="License"></a>
  </p>
  <p>
    <a href="https://arxiv.org/abs/...">Paper</a> |
    <a href="https://project-page.example">Project Page</a> |
    <a href="docs/reproduction.md">Reproduce</a> |
    <a href="#pretrained-models">Checkpoints</a> |
    <a href="#citation">Citation</a>
  </p>
  <p>
    <img src="assets/figures/teaser.png" alt="Qualitative results from Project Name" width="900">
  </p>
</div>
```

### At-A-Glance Cards

Use this near the top when a repo has concrete model/task metadata:

```markdown
<table>
  <tr>
    <td><strong>Task</strong><br>Object detection</td>
    <td><strong>Model</strong><br>Transformer detector</td>
    <td><strong>Datasets</strong><br>COCO, LVIS</td>
  </tr>
  <tr>
    <td><strong>Best result</strong><br>52.1 box AP</td>
    <td><strong>Checkpoints</strong><br>3 pretrained variants</td>
    <td><strong>Runtime</strong><br>1x GPU inference path</td>
  </tr>
</table>
```

### Research Snapshot Cards

```markdown
<table>
  <tr>
    <td><strong>Task</strong></td>
    <td>Semantic segmentation / object detection / restoration</td>
  </tr>
  <tr>
    <td><strong>Backbone</strong></td>
    <td>ViT-B / ResNet-50 / custom encoder</td>
  </tr>
  <tr>
    <td><strong>Datasets</strong></td>
    <td>Cityscapes, COCO, custom dataset</td>
  </tr>
  <tr>
    <td><strong>Best result</strong></td>
    <td>88.1 mIoU on validation split</td>
  </tr>
  <tr>
    <td><strong>Runtime</strong></td>
    <td>1x A100 for training; CPU smoke test available</td>
  </tr>
</table>
```

### Example Gallery

Use this when the model produces visual outputs or the repo has demo screenshots:

```markdown
<table>
  <tr>
    <td><img src="assets/figures/example-1.png" alt="Example output 1" width="280"></td>
    <td><img src="assets/figures/example-2.png" alt="Example output 2" width="280"></td>
    <td><img src="assets/figures/example-3.png" alt="Example output 3" width="280"></td>
  </tr>
  <tr>
    <td align="center">Input</td>
    <td align="center">Prediction</td>
    <td align="center">Overlay</td>
  </tr>
</table>
```

### Feature Cards

```markdown
<table>
  <tr>
    <td width="33%"><strong>Reproducible</strong><br>Published configs and exact eval commands.</td>
    <td width="33%"><strong>Ready to use</strong><br>Pretrained checkpoints and inference script.</td>
    <td width="33%"><strong>Extensible</strong><br>Modular datasets, models, losses, and metrics.</td>
  </tr>
</table>
```

### Model Cards In README

Use compact cards when there are only a few checkpoints:

```markdown
<table>
  <tr>
    <td>
      <strong>Base Model</strong><br>
      Dataset: COCO<br>
      Metric: 42.0 mAP<br>
      <a href="#">checkpoint</a> | <a href="configs/base.yaml">config</a>
    </td>
    <td>
      <strong>Large Model</strong><br>
      Dataset: COCO<br>
      Metric: 45.8 mAP<br>
      <a href="#">checkpoint</a> | <a href="configs/large.yaml">config</a>
    </td>
  </tr>
</table>
```

Use Markdown tables when there are many checkpoints.

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

Use cards for one to three models and tables when there are multiple models:

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
- Prefer task/model cards for important facts instead of long prose.
- Use a result card or table for headline metrics; do not bury metrics in paragraphs.
- Add an example gallery when the project is visually inspectable.
- Use badges for navigation/status, not decoration.
- Keep images committed under `assets/figures/` when small; use external hosting or releases for large files.
- Prefer short paragraphs, tables, and command blocks.
- Keep heading levels consistent.
- Avoid walls of badges, huge GIFs, uncompressed images, and long changelogs above usage instructions.
- Avoid fake UI polish: no invented results, no generic stock-like images, no decorative images unrelated to the model output.

## Image Requirements

Primary image quality matters:

- Use real qualitative outputs, architecture diagrams, benchmark visualizations, or demo screenshots.
- Add alt text that describes what the image shows.
- Keep width reasonable with HTML, usually `width="900"` for a centered hero image.
- Store small images under `assets/figures/`; put large images in releases, docs hosting, or external artifact storage.
- If results are privacy-sensitive or licensed, use diagrams or synthetic examples instead of restricted data.

## README Polish Checklist

- [ ] The first screen has a centered title, short claim, link hub, and visual.
- [ ] A new user can identify task, model type, dataset, best result, and checkpoint availability without scrolling far.
- [ ] Quickstart appears before long installation/reproduction detail.
- [ ] Checkpoints are shown as cards or tables with config, dataset, metric, and link.
- [ ] Results are shown as cards or tables with exact eval command or config.
- [ ] Images have useful alt text and point to real repository assets.
- [ ] The README links to deeper docs instead of becoming a long paper appendix.
- [ ] No fake metrics, fake screenshots, or unverifiable claims are introduced.

## Citation Section

Include both `CITATION.cff` and BibTeX when there is a paper:

```text
## Citation

If this repository helps your research, please cite:

    @inproceedings{...}
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
