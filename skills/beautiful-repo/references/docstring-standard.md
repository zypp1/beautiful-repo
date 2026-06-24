# Docstring Standard

Use this reference when adding, auditing, or improving Python docstrings in a deep learning repository.

The policy combines PEP 257, Ruff/pydocstyle public-docstring rules, PyTorch-style Google docstrings, Hugging Face-style consistency for repeated model arguments, NumPy/numpydoc readability principles, and conventions observed in high-impact repositories such as Transformers, Diffusers, MMDetection, Detectron2, MONAI, TorchVision, Lightning, timm, and nnU-Net.

## Core Rule

Docstrings are concise API contracts, not decorative comments or documentation padding.

Keep top-of-file module docstrings and function docstrings brief. The goal is the shortest text that accurately states the contract a caller or maintainer needs. Prefer one precise paragraph plus short `Args`/`Returns` sections over long explanations.

Add or improve a docstring when it helps a reader answer one of these questions without reading the whole implementation:

- What does this module/class/function own?
- What are the public inputs and outputs?
- What tensor shapes, dtypes, devices, coordinate systems, units, or value ranges are expected?
- What config keys, checkpoint formats, dataset fields, or filesystem paths are required?
- What side effects happen: training state mutation, logging, file writes, downloads, random seeds, CUDA/distributed initialization?
- What metric, protocol, or split is being measured?
- What assumptions would break reproduction if guessed incorrectly?

Do not add docstrings that merely restate the name.

## Brevity Rules

- Start with a one-line summary under 72 characters when practical.
- Keep module docstrings to 1-3 short paragraphs unless the file is a public CLI or complex integration boundary.
- Keep function docstrings focused on contract: purpose, non-obvious arguments, return value, raised errors, side effects, and deep learning tensor/config details.
- Omit `Args` entries for obvious parameters only when the project style allows it and the type/name already carries the contract.
- Prefer exact compact notation such as ``(B, C, H, W)``, ``float32``, ``[0, 1]``, and ``output_dir`` over prose.
- Move tutorials, long examples, derivations, paper background, and reproduction walkthroughs out of code. Put them in README only when they are essential to first use; otherwise leave them to substantial docs if the repo already has them.
- Delete filler such as "This function is used to", "This module contains", "Helper for", and implementation narration.

Good concise module docstring:

```python
"""Cityscapes segmentation dataset and batch collation utilities."""
```

Good concise function docstring:

```python
def compute_dice(logits: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """Compute macro Dice from ``(B, K, H, W)`` logits and ``(B, H, W)`` labels."""
```

Expand only when the compact form hides important contracts such as batch dictionary keys, checkpoint compatibility, random state, file writes, or metric protocol.

## Module Docstrings

Every public Python module should start with a module docstring after any shebang or encoding comment and before imports, including `from __future__` imports.

Use module docstrings for files under package code, scripts, tools, configs-as-code, and reusable notebooks converted to Python. Test files may stay undocumented unless they define reusable fixtures, test utilities, or public examples.

### Module Docstring Contract

A useful module docstring includes only the relevant parts:

- One-line purpose: the responsibility of the file.
- Public surface: exported classes/functions or CLI command.
- Domain contract: tensor conventions, batch schema, dataset format, metric protocol, or config schema.
- Side effects: file writes, downloads, checkpoint loading, logging, CUDA/distributed initialization, random seeding.
- Usage note: command example for scripts, or import example for library modules when helpful.

Avoid vague module summaries:

```python
"""Utils."""
```

Prefer a concise contract:

```python
"""Cityscapes-style segmentation dataset utilities.

Expects ``images/{split}`` and ``masks/{split}``. Returns image tensors as
``float32`` ``(C, H, W)`` in ``[0, 1]`` and masks as ``int64`` ``(H, W)``.
"""
```

For scripts, make the module docstring act like a usage message:

```python
#!/usr/bin/env python3
"""Evaluate a checkpoint on a configured validation split.

Example:
    python scripts/eval.py --config configs/cityscapes.yaml \
        --checkpoint checkpoints/best.pt

The script writes metrics JSON and qualitative overlays to ``output_dir`` from
the config. It does not download datasets or modify checkpoints.
"""
```

## Improving Existing Docstrings

Do not treat an existing docstring as done. First classify it:

- Missing: no docstring on a public module/class/function.
- Thin: one-line text that only restates the object name or says "helper", "wrapper", "utils", "process data", "run model", "train", or "calculate loss".
- Stale: mentions parameters, return values, defaults, shapes, paths, or metrics that no longer match the code.
- Incomplete: describes purpose but omits tensor shape/dtype/device, batch keys, config keys, side effects, or metric protocol that callers must know.
- Overspecified: duplicates obvious implementation details while omitting the external contract.
- Verbose: accurate but too long for the contract it describes; move background, examples, and implementation details to docs.

Improve in this order:

1. Preserve any correct domain meaning already present.
2. Read the signature, call sites, tests, config files, and README before editing the docstring.
3. Add only contract information that is supported by code or documentation.
4. Prefer exact shapes and keys over prose when they are known.
5. State uncertainty explicitly if the code permits multiple layouts.
6. Remove filler and implementation narration.
7. Keep pure style/docstring edits separate from mathematical or training behavior changes.

Never "fix" a docstring by guessing model math, metric definitions, label encodings, dataset splits, or checkpoint compatibility. If the contract is unclear, add a TODO in the audit report or ask the user; do not invent a false guarantee.

## Public API Docstrings

Use one consistent style in a repository. Prefer Google style when the project has no existing convention; use NumPy style if the project already uses numpydoc/Sphinx conventions.

For public functions and methods, include:

- Short summary in imperative or descriptive voice.
- `Args`/`Parameters` for non-obvious inputs.
- `Returns`/`Yields` for non-`None` outputs.
- `Raises` for user-facing validation errors.
- Shape/dtype/device/value range for tensors.
- Units and coordinate systems for boxes, masks, images, time, distance, or medical spacing.
- Side effects when the function writes files, logs, downloads, mutates state, changes random seeds, or initializes distributed/CUDA state.

Example:

```python
def compute_multiclass_dice(
    logits: torch.Tensor,
    target: torch.Tensor,
    num_classes: int,
    ignore_index: int | None = None,
) -> torch.Tensor:
    """Compute mean Dice score from segmentation logits.

    Args:
        logits: Float tensor of shape ``(B, K, H, W)`` containing unnormalized
            class logits.
        target: Integer tensor of shape ``(B, H, W)`` containing class IDs in
            ``[0, K - 1]``. Pixels equal to ``ignore_index`` are excluded.
        num_classes: Number of semantic classes ``K``.
        ignore_index: Optional target value to exclude from both numerator and
            denominator.

    Returns:
        Scalar tensor with the macro-averaged Dice score. Higher is better.
    """
```

## Class Docstrings

For public classes, document construction-time contract and runtime behavior:

- What role the class plays: dataset, model, transform, loss, metric, trainer, callback, config object.
- Required constructor arguments and defaults that affect reproducibility.
- Tensor layout expected by `forward`, `__call__`, or `__getitem__`.
- Mutable state, buffers, registered modules, cached files, or distributed assumptions.
- Checkpoint or serialization compatibility.

For model classes, do not repeat every layer. Explain the architecture family, expected input/output tensors, config knobs, and checkpoint compatibility.

## Domain-Specific Requirements

### Dataset And Dataloader Modules

Document:

- Expected directory layout or manifest columns.
- Split names and how they map to files.
- Returned sample keys.
- Image/mask/token shapes, dtypes, value ranges, and units.
- Transform randomness and whether deterministic evaluation is supported.
- Download, cache, or preprocessing side effects.

### Model Modules

Document:

- Input layout such as ``(B, C, H, W)``, ``(B, T, D)``, or token IDs ``(B, T)``.
- Output structure: logits, features, embeddings, masks, boxes, losses, hidden states.
- Config object or constructor keys that change architecture.
- Device/dtype assumptions for mixed precision, quantization, or export.
- Checkpoint key compatibility and strict/non-strict loading.

### Loss And Metric Modules

Document:

- Mathematical target in words, not a derivation dump.
- Expected logits/probabilities/labels and reduction mode.
- Ignore labels, class weights, averaging mode, smoothing constants.
- Whether higher/lower is better for metrics.
- Dataset split/protocol when metric values are compared in README tables.

### Training And Evaluation Modules

Document:

- Required batch keys and config sections.
- State mutations: optimizer, scaler, scheduler, EMA, gradient accumulation.
- Random seed, deterministic mode, distributed assumptions, and checkpoint writes.
- Return values and logged metrics.

### Inference And Demo Modules

Document:

- Accepted input formats and preprocessing.
- Output files or returned objects.
- Checkpoint/model-id loading behavior.
- CPU/GPU requirements and batch-size constraints.

### Config And Checkpoint Modules

Document:

- Required keys, defaults, and unknown-key behavior.
- Path resolution rules.
- Version/schema compatibility.
- Whether loading mutates global state or downloads weights.

## Thin Docstring Heuristics

Flag an existing docstring for improvement when any of these are true:

- The summary is fewer than five words for a public object with arguments or returns.
- The summary only expands the function/class name.
- It uses generic words such as "utils", "helper", "wrapper", "process", "run", "do", or "handle" without a domain object.
- It has `Args` or `Returns` sections with empty or placeholder descriptions.
- It documents `x`, `data`, or `batch` without shape, keys, dtype, or value range.
- It says "prediction", "target", "label", "mask", "image", "checkpoint", or "config" without explaining format.
- It omits side effects for file I/O, downloads, random seeds, CUDA/distributed initialization, or logging.
- It disagrees with the function signature, tests, or README commands.

Use these heuristics as review prompts, not absolute blockers. A small private helper can remain undocumented when its name and surrounding code are clear.

## Anti-Patterns

Avoid:

- Long docstrings that paraphrase every implementation line.
- Module or function docstrings that read like README sections.
- Fake precision: claiming a tensor shape or metric protocol that the code does not enforce.
- Copy-pasted parameter docs that no longer match defaults.
- "This function..." boilerplate when the summary can start with the verb or noun directly.
- Duplicating README tutorials inside low-level API docstrings.
- Mixing Google and NumPy styles in one file without a project precedent.
- Adding docstring-only churn to generated code or vendored code.

## Review Checklist

Before considering docstring work complete:

- Public modules have top-of-file docstrings.
- Public classes/functions have docstrings unless the repository convention intentionally excludes them.
- Existing docstrings were checked for thin/stale/incomplete content, not only presence.
- Module and function docstrings are concise; long background or examples moved out of code.
- Tensor contracts include shapes, dtypes, devices, value ranges, and batch keys where relevant.
- Data, checkpoint, config, metric, and side-effect contracts are explicit.
- Tests or call sites support any newly documented behavior.
- No training behavior, math, default hyperparameters, or random-seed behavior changed during docstring cleanup.
