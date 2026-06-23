<div align="center">
  <h1>Project Name</h1>
  <p><strong>Short task/model claim in one sentence.</strong></p>
  <p>
    <a href="https://arxiv.org/abs/...">Paper</a> |
    <a href="https://project-page.example">Project Page</a> |
    <a href="docs/reproduction.md">Reproduce</a> |
    <a href="#pretrained-models">Checkpoints</a> |
    <a href="#citation">Citation</a>
  </p>
  <p>
    <img src="assets/figures/teaser.png" alt="Representative qualitative results from Project Name" width="900">
  </p>
</div>

## Snapshot

<table>
  <tr>
    <td><strong>Task</strong></td>
    <td>Semantic segmentation / detection / restoration / classification</td>
  </tr>
  <tr>
    <td><strong>Model</strong></td>
    <td>Backbone and method family</td>
  </tr>
  <tr>
    <td><strong>Datasets</strong></td>
    <td>Dataset names and splits</td>
  </tr>
  <tr>
    <td><strong>Best result</strong></td>
    <td>Metric on the main benchmark</td>
  </tr>
  <tr>
    <td><strong>Runtime</strong></td>
    <td>Training/evaluation hardware assumptions</td>
  </tr>
</table>

## Highlights

<table>
  <tr>
    <td width="33%"><strong>Reproducible</strong><br>Published configs and exact eval commands.</td>
    <td width="33%"><strong>Ready to use</strong><br>Pretrained checkpoints and inference script.</td>
    <td width="33%"><strong>Extensible</strong><br>Modular datasets, models, losses, and metrics.</td>
  </tr>
</table>

## Quickstart

```bash
python -m pip install -e ".[dev]"
python scripts/infer.py \
  --config configs/demo.yaml \
  --checkpoint checkpoints/demo.pt \
  --input assets/examples/example.jpg \
  --output outputs/demo
```

## Pretrained Models

<table>
  <tr>
    <td>
      <strong>Base Model</strong><br>
      Dataset: Dataset name<br>
      Metric: 0.00 main metric<br>
      <a href="#">checkpoint</a> · <a href="configs/base.yaml">config</a>
    </td>
    <td>
      <strong>Large Model</strong><br>
      Dataset: Dataset name<br>
      Metric: 0.00 main metric<br>
      <a href="#">checkpoint</a> · <a href="configs/large.yaml">config</a>
    </td>
  </tr>
</table>

## Reproducing Results

| Setting | Config | Checkpoint | Command | Metric | Expected |
| --- | --- | --- | --- | --- | --- |
| Main result | `configs/main.yaml` | `model.pt` | `python scripts/eval.py --config configs/main.yaml --checkpoint model.pt` | Metric | 0.00 |

## Citation

If this repository helps your research, please cite:

```bibtex
@inproceedings{example,
  title = {Project Title},
  author = {Author, A.},
  year = {2026}
}
```
