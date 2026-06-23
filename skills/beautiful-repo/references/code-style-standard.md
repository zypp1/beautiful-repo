# Code Style Standard

Use this reference before editing Python code internals, names, docstrings, type hints, or module boundaries.

## Default Policy

- Match the repository's existing style if it is coherent.
- If style is absent or inconsistent, converge on PEP 8 naming/layout, PEP 257 docstring basics, Ruff for lint/format, and pytest for tests.
- Prefer clear, small changes over mass rewrites. Keep behavior-preserving style changes separate from experiment logic changes.
- Add types and docstrings to public modules and APIs first: datasets, models, losses, metrics, trainers, evaluators, config loaders, and CLI entry functions.
- Do not change mathematical expressions, tensor layouts, default hyperparameters, or random seed behavior during pure style cleanup.

## Naming

Use names that reveal domain role:

- dataset objects: `train_dataset`, `val_dataset`, `test_dataset`
- tensors: `images`, `tokens`, `labels`, `logits`, `features`, `embeddings`, `masks`
- shapes: `batch_size`, `num_channels`, `height`, `width`, `num_classes`
- config: `config`, `model_config`, `data_config`, `train_config`
- devices: `device`, `dtype`, `precision`
- paths: `data_root`, `checkpoint_path`, `output_dir`

Avoid vague public names: `foo`, `bar`, `tmp`, `data`, `res`, `out`, `obj`, `thing`, `processor` when a specific role is known.

Short mathematical names such as `x`, `y`, `z`, `q`, `k`, `v` are acceptable inside short tensor expressions when shape and meaning are obvious from context. Avoid them in public function signatures unless they mirror established framework APIs.

Read `naming-standard.md` before doing a naming pass across directories, Python files, public APIs, configs, experiment names, CLI flags, or output artifacts. Treat public renames as migrations: search references, preserve old commands when needed, and keep rename-only changes separate from behavior changes.

## Function Boundaries

Split functions when they mix responsibilities:

- argument parsing
- config loading
- dataset construction
- model construction
- checkpoint loading
- training loop
- evaluation loop
- logging
- visualization

Entrypoint scripts should be thin. They should parse args, load config, call package functions, and exit.

Prefer pure helpers for:

- metric calculations
- transforms
- model factory logic
- scheduler/optimizer construction
- checkpoint path resolution

Keep side effects explicit: filesystem writes, downloads, CUDA initialization, logging setup, random seed setting, and distributed initialization should happen inside named functions, not at import time.

## Docstrings

Use docstrings for public modules, classes, and functions. Private one-line helpers can remain undocumented when their names are clear.

Read `docstring-standard.md` before doing a docstring pass. It defines module-level docstrings, thin/stale docstring detection, and domain-specific contracts for datasets, models, losses, metrics, training, evaluation, inference, configs, and checkpoints.

Every public Python module should start with a file-level docstring that states what the file owns. For scripts, the top docstring should also name the CLI behavior and side effects. Avoid vague summaries such as `"""Utilities."""`; state the task, data contract, and important side effects when known.

For deep learning code, useful docstrings include:

- tensor shapes and axis conventions
- dtype and device expectations
- accepted config keys
- randomness and deterministic behavior
- filesystem/network side effects
- checkpoint compatibility
- metric definitions and units

Existing docstrings still need review. Improve thin docstrings that only restate the object name, use vague words such as "helper" or "process data", omit tensor/config/checkpoint contracts, or no longer match the signature, tests, configs, or README commands.

Prefer Google or NumPy style consistently within a repository. Do not mix styles in one module unless the project already does.

### Deep Learning Docstring Contract

For public data/model/loss/metric/training APIs, include the pieces that affect reproducibility:

- Tensor shapes use explicit conventions such as `(batch, channels, height, width)` or `(batch, sequence, hidden)`.
- State layout aliases once per module: `B`, `C`, `H`, `W`, `T`, `D`, `K`, and `num_classes`.
- State dtype and value range for image tensors, masks, token IDs, logits, probabilities, and labels.
- State device expectations when CPU/GPU placement matters.
- For batch dictionaries, document required keys, optional keys, shapes, dtypes, and units.
- For config inputs, document required keys, defaults, and whether unknown keys are rejected.
- For checkpoints, document expected state dict keys, version compatibility, strict/non-strict loading, and side effects.
- For metrics, document exact definition, averaging mode, unit, split/protocol, and whether higher is better.
- For stochastic transforms or training utilities, document randomness, seeds, deterministic mode, and distributed assumptions.

Example batch contract:

```python
def training_step(batch: dict[str, torch.Tensor], model: torch.nn.Module) -> torch.Tensor:
    """Run one supervised training step.

    Args:
        batch: Mini-batch with keys:
            ``image``: Float tensor of shape ``(B, 3, H, W)`` in ``[0, 1]``.
            ``mask``: Long tensor of shape ``(B, H, W)`` with class IDs.
        model: Segmentation model returning logits of shape ``(B, K, H, W)``.

    Returns:
        Scalar loss tensor on the same device as ``batch["image"]``.
    """
```

Example:

```python
def compute_dice_score(
    pred_mask: torch.Tensor,
    target_mask: torch.Tensor,
    epsilon: float = 1e-6,
) -> torch.Tensor:
    """Compute the mean Dice score for binary segmentation masks.

    Args:
        pred_mask: Predicted mask tensor with shape ``(N, H, W)`` or
            ``(N, 1, H, W)``. Values are expected to be binary or probabilities.
        target_mask: Ground-truth mask tensor with the same shape as
            ``pred_mask``.
        epsilon: Small constant used to avoid division by zero.

    Returns:
        Scalar tensor containing the batch-mean Dice score.
    """
```

## Type Hints

Add type hints where they clarify contracts:

- config objects and dictionaries
- paths: `str | Path`
- public return values
- tensors in model/loss/metric APIs when useful

Do not overfit hints to one framework version. Use flexible protocols or simple annotations when dynamic framework objects would make hints brittle.

## Imports

- Keep imports at top level unless importing an optional heavy dependency or avoiding framework startup cost.
- Avoid wildcard imports.
- Avoid modifying `sys.path` in library code. If the repository needs package imports, fix packaging or editable install instructions.
- Keep optional dependencies behind clear error messages.

## Error Messages

Make errors actionable:

- include the missing path, expected layout, and doc section
- include the config key that failed validation
- explain CPU/GPU requirement mismatches
- avoid bare `assert` for user-facing validation in scripts

## Code Smells To Fix

Prioritize:

- large training scripts with mixed config/model/data/eval logic
- import-time checkpoint loading or dataset download
- author-local absolute paths
- duplicated metric implementations
- hidden global config or mutable module-level state
- vague variable names in public APIs
- public functions/classes without docstrings
- no dry-run/help path for CLIs

Defer:

- wholesale architecture rewrites
- changing trainer framework
- replacing all configs
- converting all docs to one docstring style
- adding strict typing everywhere at once
