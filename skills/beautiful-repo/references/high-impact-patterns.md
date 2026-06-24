# High-Impact Repository Patterns

Use this reference before claiming that a change follows "standard deep learning repository" practice.

This skill is based on a representative comparison of high-impact deep learning repositories and official standards, not on a single template. The sample includes:

- Hugging Face Transformers and Diffusers: strong README first screen, installation, quick tours, examples, docs, modular package structure, and large model ecosystem.
- OpenMMLab MMDetection: configs, tools, docs, model zoo, dataset/model indexes, tests, pre-commit, and citation metadata.
- Detectron2: install docs, tutorials, model zoo/baselines, license, and citation.
- Segment Anything and CLIP: paper/project/demo/model-card links, checkpoint instructions, example notebooks, BibTeX, and visual assets.
- timm: model collection, pretrained weights, reference train/validation scripts, and reproducibility-oriented results.
- Ultralytics: clear task modes such as train, validate, predict, export, and benchmark.
- nnU-Net and MONAI: domain-specific dataset preparation, preprocessing, training, inference, medical-imaging constraints, docs, tests, and citations.
- PyTorch Lightning and TorchVision: package structure, docs, examples, tests, CI, model references, and contribution metadata.
- PEP 8, PEP 257, Google Python style guidance, numpydoc, Ruff, pytest, Python packaging, pre-commit, and GitHub README/CITATION/license/contribution docs.
- High-star README presentation samples including LangChain, Dify, Gradio, Streamlit, Next.js, Stable Diffusion WebUI, Ultralytics, Segment Anything, and MMDetection.

## Common Patterns Worth Emulating

Adopt these patterns when they fit the target repository:

- First screen: centered project identity, short value proposition, badge row, real paper/project/demo/model/data/checkpoint links, and one real visual that shows model/task output.
- Fast path: install command plus a minimal inference or smoke-test command that users can run quickly.
- Full path: separate training, evaluation, inference, export, and reproduction commands.
- Artifact path: documented dataset layout, checkpoint table, pretrained weight download, and result table.
- Research path: paper links, BibTeX, `CITATION.cff`, license, model/data cards, and known limitations.
- Developer path: package layout, tests, lint/format, CI, contributing notes, and issue/reporting paths.
- Scale path: configs or recipes for published models, not one-off hard-coded scripts.

## High-Star README Presentation Patterns

Apply these visual patterns when polishing a README:

- Center the hero block. Use the project name, one strong sentence, badges, and 4-7 primary links before any long prose.
- Show, then explain. Put a teaser image, result grid, product screenshot, architecture figure, or demo GIF above installation.
- Use cards for scanning. Use HTML tables to create stable GitHub-rendered cards for features, tasks, datasets, model variants, and results.
- Put a short Quickstart early. A copy-paste install plus one inference/demo command should appear before long setup notes.
- Separate "try it" from "reproduce it." Quickstart should be short; paper reproduction belongs in a README section or a substantial reproduction document only when that file already carries real detail.
- Use visual proof carefully. Screenshots and result images must reflect real outputs, not decorative stock images or invented metrics.
- Route deep content away from the first screen. Long dataset instructions, benchmarks, API details, and ablations belong in later README sections or substantial local docs when the repository already has them.
- Make model access obvious. Checkpoint cards/tables should include config, dataset, metric, and download link.
- Keep social/community links compact. Discord, discussions, docs, examples, and issues are useful; a badge wall is not.

## Patterns To Avoid

Do not blindly copy:

- Heavy framework stacks from large libraries into a small paper repo.
- Model-zoo complexity when the project has one model.
- Badge walls, logos, or animations that push install/use instructions below the fold.
- Decorative images that do not reveal the model, product, task, dataset, or result.
- Cards that repeat claims but omit install, checkpoints, metrics, or reproduction paths.
- CI that requires private datasets, GPUs, unavailable secrets, or heavyweight installs on every small-repo push.
- Notebook-only workflows.
- Research claims without the exact command, checkpoint, dataset split, and metric implementation needed to verify them.

## Evidence-Based Audit Questions

Ask these during review:

- Can a first-time user understand the task, paper, model, and demo path in under one minute?
- Is there a CPU-friendly or explicitly GPU-scoped smoke command?
- Are configs tied to published results or representative experiments?
- Are data and checkpoint layouts documented without relying on author-local paths?
- Can a reviewer inspect model/data limitations before using pretrained weights?
- Can contributors run tests and lint locally without full datasets?
- Do public functions/classes explain tensor shapes, devices, dtypes, randomness, and side effects where relevant?
