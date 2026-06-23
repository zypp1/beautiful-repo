# Sources Reviewed

Use this file to understand the evidence base behind the skill. The list is representative, not exhaustive.

## High-Impact Deep Learning Repositories

- Hugging Face Transformers: https://github.com/huggingface/transformers
- Hugging Face Diffusers: https://github.com/huggingface/diffusers
- OpenMMLab MMDetection: https://github.com/open-mmlab/mmdetection
- Detectron2: https://github.com/facebookresearch/detectron2
- Segment Anything: https://github.com/facebookresearch/segment-anything
- timm / pytorch-image-models: https://github.com/huggingface/pytorch-image-models
- Ultralytics: https://github.com/ultralytics/ultralytics
- nnU-Net: https://github.com/MIC-DKFZ/nnUNet
- MONAI: https://github.com/Project-MONAI/MONAI
- PyTorch Lightning: https://github.com/Lightning-AI/pytorch-lightning
- TorchVision: https://github.com/pytorch/vision
- CLIP: https://github.com/openai/CLIP
- Qwen: https://github.com/QwenLM/Qwen

## High-Star README Design Samples

- Awesome LLM Apps: https://github.com/Shubhamsaboo/awesome-llm-apps
- LangChain: https://github.com/langchain-ai/langchain
- Dify: https://github.com/langgenius/dify
- Gradio: https://github.com/gradio-app/gradio
- Streamlit: https://github.com/streamlit/streamlit
- Next.js: https://github.com/vercel/next.js
- Stable Diffusion WebUI: https://github.com/AUTOMATIC1111/stable-diffusion-webui
- Ultralytics: https://github.com/ultralytics/ultralytics
- Segment Anything: https://github.com/facebookresearch/segment-anything
- MMDetection: https://github.com/open-mmlab/mmdetection
- Awesome README: https://github.com/matiassingers/awesome-readme
- Open Model Zoo: https://github.com/openvinotoolkit/open_model_zoo
- ONNX Model Zoo: https://github.com/onnx/models

Use these for presentation patterns: centered hero blocks, logo or output images, badges, compact link hubs, short install paths, demo screenshots/GIFs, feature cards, example galleries, model/result tables, and links to deeper docs. Do not copy content claims.

## Official Standards And Tooling Docs

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/
- Python tutorial on modules: https://docs.python.org/3/tutorial/modules.html
- PyTorch docstring guidelines: https://github.com/pytorch/pytorch/wiki/Docstring-Guidelines
- Google Python style guide docstrings: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
- NumPy docstring guide: https://numpydoc.readthedocs.io/en/latest/format.html
- Ruff pydocstyle rules: https://docs.astral.sh/ruff/rules/#pydocstyle-d
- GitHub README docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- GitHub citation file docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- Ruff configuration: https://docs.astral.sh/ruff/configuration/
- pytest good practices: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- Python packaging `pyproject.toml`: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- pre-commit: https://pre-commit.com/

## How To Use This List

Do not copy any single repository wholesale. Use the common patterns:

- clear first-screen README signal
- visual hero with real product/model output
- badge row and compact documentation link hub
- feature cards or use-case cards for fast scanning
- screenshots, qualitative result grids, or demo GIFs
- quickstart before long documentation
- stable train/eval/infer commands
- configs tied to results
- checkpoint and dataset tables
- docs for setup, data, reproduction, and results
- package-quality Python code
- consistent directory, Python file, package, function, class, constant, config, and experiment naming
- public module/class/function docstrings that document API contracts, not just names
- tensor shapes, dtypes, devices, config keys, checkpoint compatibility, metrics, randomness, and side effects in deep learning docstrings
- smoke tests and CI that do not require full datasets by default
- citation, license, and contribution metadata

## Docstring Pattern Notes

- PEP 257 and Ruff/pydocstyle treat missing public module, class, method, and function docstrings as explicit documentation quality signals.
- PyTorch's docstring guidance favors Google-style sections, semantic argument descriptions, examples where useful, and avoiding repetitive or misleading parameter text.
- Hugging Face libraries emphasize consistent descriptions for repeated model/config arguments and clear examples for user-facing APIs.
- OpenMMLab, Detectron2, MONAI, TorchVision, Lightning, timm, and nnU-Net commonly make data/model/metric contracts discoverable through module structure, class/function docstrings, config docs, and README/model-zoo tables.
- For deep learning repositories, docstring quality depends on contract precision: tensor layout, dtype, value range, batch keys, metric protocol, checkpoint compatibility, randomness, and side effects matter more than docstring length.

## README Pattern Notes

The README guidance intentionally combines research-code patterns with polished product README patterns:

- Transformers-style libraries emphasize a short promise, installation compatibility, quick usage, and links to a broader model/checkpoint ecosystem.
- Awesome LLM Apps-style curated READMEs use emoji-led category navigation, visual section anchors, dense resource tables, and approachable scanning for broad audiences.
- Qwen-style model READMEs use strong project identity, platform/model links, news, quickstart, model tables, and multilingual/community entry points.
- Dify, Gradio, and Streamlit-style product READMEs use a strong first-screen identity, screenshots or demos, compact links, quickstart, and feature cards.
- Ultralytics and OpenMMLab-style vision/model-zoo READMEs make docs, installation, model zoo, training, prediction, and deployment paths visible early.
- Segment Anything-style research releases make paper/project/demo/dataset links, visual outputs, getting-started examples, and checkpoint access obvious.
- GitHub README and citation guidance supports keeping the repository README discoverable, rendered with GitHub Markdown, and paired with `CITATION.cff` when citation matters.

Translate those patterns into repo-type-specific layouts instead of forcing every deep learning repo into the same README shape.
