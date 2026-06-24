# Research Release Standard

Use this reference for paper, benchmark, model zoo, and reproducibility-oriented deep learning repositories.

## README Contract

The README should let a new researcher decide whether the repository is relevant and reproduce a minimal result.

Required sections:

- Project title and one-paragraph scope.
- Paper link, project page, or arXiv link when available.
- Installation with Python version, CUDA/PyTorch/TensorFlow compatibility, and dependency command.
- Dataset preparation with source links, expected layout, preprocessing commands, and licensing caveats.
- Quickstart that runs on a tiny sample, synthetic sample, or documented demo input.
- Training command with the default config.
- Evaluation command with expected metric names and approximate published values.
- Inference/demo command for pretrained weights when available.
- Checkpoint download table with model name, dataset, metric, file size, and checksum when available.
- Results table matching paper claims or clearly explaining differences.
- Citation section with BibTeX and `CITATION.cff`.
- License and acknowledgement.

## Reproducibility Checklist

Record or implement:

- Random seed handling for Python, NumPy, framework RNGs, dataloaders, and distributed training.
- Exact dependency versions or a lock file.
- Hardware assumptions: GPU model/count, CUDA version, memory needs, expected runtime.
- Data version, preprocessing version, splits, and filtering rules.
- Training schedule: batch size, gradient accumulation, optimizer, learning rate schedule, epochs/steps, precision, and augmentation.
- Evaluation protocol: checkpoint selection, test-time augmentation, metric implementation, thresholding, and post-processing.
- Published configs for headline results.
- Known nondeterminism and expected metric tolerance.

## Configuration Standard

Prefer a single config object loaded by training, evaluation, and inference.

Recommended fields:

```yaml
seed: 42
project:
  name: example
paths:
  data_root: data/example
  output_dir: outputs/example
model:
  name: example_model
data:
  dataset: example_dataset
  train_split: train
  val_split: val
training:
  epochs: 100
  batch_size: 32
  optimizer: adamw
  lr: 0.0001
evaluation:
  metrics: [accuracy]
runtime:
  device: cuda
  precision: fp32
```

Avoid config values that depend on the author's local absolute paths.

## Tests For Research Code

Prioritize tests that catch broken releases:

- `test_imports.py`: import the package and important modules.
- `test_config_load.py`: parse default and representative experiment configs.
- `test_model_forward.py`: construct a small model or production model with tiny input and run one forward pass.
- `test_dataset_smoke.py`: load a synthetic/tiny fixture or validate error messages when data is absent.
- `test_metrics.py`: verify metric behavior on known tiny arrays.
- `test_cli_smoke.py`: run `--help` or dry-run modes for train/eval/infer scripts.

Do not require full datasets or GPUs for default CI tests unless unavoidable.

For tiny or small releases, keep push CI cheap: metadata checks, Python syntax, import smoke tests, and maybe the fastest unit tests. Run heavier checks, dependency installs, model-forward smoke tests, and audit scripts on pull requests, scheduled jobs, manual dispatch, or before tagging a release.

## Release Metadata

Add `CITATION.cff` for repositories intended to be cited. Include title, authors, release date, version, repository URL, DOI when available, and preferred citation.

For pretrained models, add a model card or `docs/model_card.md` with:

- Model purpose and intended use.
- Training data summary.
- Metrics and evaluation protocol.
- Limitations and failure modes.
- Checkpoint download and license.

For datasets or derived splits, add a data card or `docs/data.md` with:

- Data source and license.
- Download and preprocessing.
- Expected layout.
- Splits and leakage precautions.
- Ethics/privacy notes when relevant.
