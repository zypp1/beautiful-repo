# Naming Standard

Use this reference when normalizing directory names, Python file names, public APIs, config names, experiment names, and generated artifact paths in a deep learning repository.

Naming changes are migrations. Rename only when the new name improves discoverability or prevents ambiguity, and preserve old commands or document the replacement.

## Core Policy

- Prefer the repository's existing coherent convention over a wholesale rename.
- Use PEP 8 names for Python code when no local convention exists.
- Keep public import paths stable unless the user approves a breaking migration.
- Separate rename-only commits from behavior changes.
- Do not rename datasets, checkpoint files, published config IDs, metric keys, model names, or paper table names when external users may already rely on them.
- Add compatibility wrappers or aliases for renamed entry points when practical.

## Directory Names

Prefer lowercase directory names with underscores only when the name is also a Python package.

Recommended deep learning directories:

```text
configs/
scripts/
src/<package_name>/
tests/
docs/
examples/
assets/
data/              # ignored or documented external artifact
checkpoints/       # ignored or documented external artifact
outputs/           # ignored generated files
```

Package subdirectories should use singular or role-based names consistently:

```text
data/
models/
losses/
metrics/
training/
evaluation/
inference/
utils/
visualization/
```

Avoid mixed naming such as `ModelZoo/`, `TrainScripts/`, `my-utils/`, `new_code/`, `final/`, `backup/`, `tmp/`, `old/`, and `misc/` unless they are explicitly archival and ignored.

## Python File And Package Names

Use lowercase `snake_case.py` for Python files and lowercase `snake_case` for packages:

- `dataset.py`, `image_dataset.py`, `modeling_unet.py`, `losses.py`, `dice_metric.py`
- `train.py`, `eval.py`, `infer.py`, `export.py`, `download_weights.py`
- package names such as `semantic_segmentation`, not `SemanticSegmentation`

Avoid:

- CamelCase Python files such as `MyModel.py`
- spaces, hyphens, dots beyond `.py`, and version suffixes in modules
- file names that collide with common packages: `torch.py`, `numpy.py`, `typing.py`, `random.py`, `utils.py` at the repository root when it shadows imports
- numbered scratch files such as `train2.py`, `test_new.py`, `final_model.py`

Allow exceptions for upstream compatibility, generated files, migration shims, and externally documented scripts.

## Public API Names

Follow PEP 8 defaults:

- packages/modules: `lower_snake_case`
- functions/methods: `lower_snake_case`
- variables/arguments: `lower_snake_case`
- classes: `CapWords`
- constants: `UPPER_SNAKE_CASE`
- private helpers: leading underscore

Deep learning public names should reveal domain role:

- datasets: `CityscapesDataset`, `build_train_dataset`, `collate_detection_batch`
- models: `UNet`, `VisionTransformer`, `build_model`, `load_pretrained_backbone`
- losses: `DiceLoss`, `compute_contrastive_loss`
- metrics: `MeanIoU`, `compute_dice_score`, `evaluate_retrieval`
- training: `train_one_epoch`, `validate_one_epoch`, `build_optimizer`
- inference: `run_inference`, `preprocess_image`, `postprocess_masks`
- checkpoints: `load_checkpoint`, `save_checkpoint`, `strip_module_prefix`
- configs: `load_config`, `validate_config`, `merge_overrides`

Avoid vague public names:

```text
foo, bar, tmp, tmp2, data, data1, res, result, out, obj, thing, helper,
processor, manager, wrapper, do_it, run_all, main_func, new_model
```

Short tensor names such as `x`, `y`, `q`, `k`, `v` are acceptable inside compact math expressions, but public signatures should prefer `images`, `tokens`, `logits`, `labels`, `features`, `attention_mask`, or another role-specific name.

## Entry Point Names

Use stable and predictable script names:

- `scripts/train.py`
- `scripts/eval.py`
- `scripts/infer.py`
- `scripts/export.py`
- `scripts/download_data.py`
- `scripts/download_weights.py`

Keep legacy entry points as wrappers when users may have copied commands from a paper, README, issue, or benchmark script.

CLI arguments should use kebab-case:

```bash
python scripts/train.py --config configs/default.yaml --output-dir outputs/debug
```

Python variables that receive those values should use snake_case:

```python
output_dir = args.output_dir
```

## Config And Experiment Names

Config files should make model, dataset, and purpose visible:

```text
configs/default.yaml
configs/cityscapes/unet_r50_512x1024.yaml
configs/imagenet/vit_b16_224.yaml
configs/experiments/ablation_no_pretrain.yaml
```

Prefer names that encode stable experiment identity, not local chronology:

- good: `unet_r50_cityscapes_512x1024.yaml`
- bad: `exp1.yaml`, `test.yaml`, `latest.yaml`, `new.yaml`, `final.yaml`

Do not rename configs that are cited by a paper, model zoo, checkpoint table, or external scripts unless compatibility aliases remain.

## Artifacts And Outputs

Generated outputs should be predictable and ignored by git:

```text
outputs/<run_name>/
logs/<run_name>/
checkpoints/<run_name>/epoch_010.pt
```

Use run names that include task-relevant identity:

```text
cityscapes_unet_r50_seed0
imagenet_vit_b16_amp
```

Avoid author-local, date-only, or ambiguous names such as `myrun`, `debug2`, `final`, `best_new`, and `2024_01_01` unless a tracker records full metadata elsewhere.

## Rename Workflow

Before renaming:

1. Search references with `rg`: imports, CLI commands, configs, README, docs, tests, CI, notebooks, and shell scripts.
2. Decide whether the name is public or private.
3. If public, add a compatibility wrapper, import alias, deprecation note, or migration note.
4. Run import tests, CLI help, and smoke commands.
5. Keep the rename commit separate from behavior changes.

After renaming, verify:

- imports still work from a fresh checkout
- documented train/eval/infer commands still work or have explicit replacements
- README links and config/checkpoint tables use the new names
- tests and CI reference the new names
- no stale names remain except intentional compatibility aliases

## Review Checklist

- Directories follow a consistent `configs/`, `src/`, `scripts/`, `tests/`, `docs/`, `examples/`, `assets/` shape where appropriate.
- Python files and package directories use lowercase snake_case.
- Public functions/methods use snake_case; classes use CapWords; constants use UPPER_SNAKE_CASE.
- Public names reveal domain role and avoid generic `data`, `result`, `processor`, or `manager` unless the scope makes them precise.
- Config and experiment names encode model/dataset/purpose rather than chronology.
- CLI flags use kebab-case and internal variables use snake_case.
- Renames preserve or document compatibility for published commands, config names, checkpoint names, and import paths.
