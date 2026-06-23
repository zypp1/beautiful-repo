# Framework Notes

Use this reference for framework-specific decisions. Prefer existing project conventions over adding a new framework.

## PyTorch

Common structure:

- `data/`: `Dataset`, datamodule-like factories, collate functions, transforms.
- `models/`: modules and model factory functions.
- `losses/`: custom losses.
- `metrics/`: metric implementations independent of training loops.
- `training/`: loop, optimizer/scheduler construction, checkpointing.
- `evaluation/`: evaluation loop and metric aggregation.
- `inference/`: preprocessing, prediction, postprocessing.

Recommended smoke tests:

- instantiate model
- run `model.eval()`
- run one forward pass with tiny tensor input
- verify output shape and dtype

Avoid:

- checkpoint loading at import time
- CUDA initialization at import time
- global mutable config
- hard-coded local dataset paths

## PyTorch Lightning

Keep Lightning modules focused:

- `LightningModule` owns model step logic, optimizer config, and metric logging.
- `LightningDataModule` owns setup, dataloaders, and transforms.
- CLI scripts own config parsing and trainer construction.

Document Lightning version because APIs can change across releases.

## Hugging Face

Record:

- model identifiers or local checkpoint layout
- tokenizer/processor identifiers
- dataset loading and preprocessing scripts
- revision hashes for remote models/datasets when reproducibility matters

For model releases, include a model card and intended-use notes.

## TensorFlow / Keras

Separate:

- model construction
- data pipeline
- training callbacks
- evaluation/inference

Record TensorFlow, CUDA, and cuDNN compatibility. Avoid graph/session assumptions unless the project uses legacy TensorFlow.

## JAX

Record:

- JAX, jaxlib, CUDA plugin, and accelerator compatibility
- PRNG key flow
- pmap/pjit assumptions
- checkpoint format and restore code

Tests should validate shape transformations and one small compiled/eager path where feasible.

## MONAI / Medical Imaging

Document:

- dataset licensing and access restrictions
- preprocessing, spacing, orientation, and intensity normalization
- train/val/test splits and leakage controls
- metric definitions and post-processing
- privacy constraints and non-distribution rules

Do not commit private medical data, derived patient data, or identifying metadata.
