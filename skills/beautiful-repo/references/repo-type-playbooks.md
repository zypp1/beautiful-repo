# Repository Type Playbooks

Use this reference immediately after classifying the repository. Pick the closest primary type, then borrow secondary checks only when they fit.

## Paper Release

Primary promise: another researcher can reproduce the paper's headline tables or figures.

Prioritize:

- `README.md` first screen with paper link, teaser/result image, main metric, checkpoints, and reproduction link.
- `docs/reproduction.md` with exact environment, data, checkpoint, training, evaluation, seeds, hardware, and expected tolerance.
- `configs/experiments/` entries for every published table row or representative ablation.
- Result table linking each number to config, checkpoint, command, split, and metric definition.
- `CITATION.cff`, BibTeX, license, acknowledgements, and limitations.

Defer:

- Broad package API polish before the paper reproduction path works.
- Converting one-off experiment code into a large framework.

## Method Or Library

Primary promise: users can import and extend reusable components.

Prioritize:

- `src/<package>/` package layout with stable module boundaries.
- Public API docstrings for models, losses, metrics, datasets, trainers, and config loaders.
- Minimal examples that import the package, instantiate a model/loss/metric, and run one forward path.
- README feature cards, API quickstart, compatibility matrix, and link to API docs.
- Unit tests for pure functions, tensor shape contracts, config parsing, and checkpoint loading.

Defer:

- Large benchmark tables unless results are central to adoption.
- Heavy demo UI work before import/API examples are clear.

## Model Zoo Or Benchmark

Primary promise: users can compare, download, and evaluate many model variants.

Prioritize:

- Model table with name, task, config, dataset, metric, checkpoint, size, license, and notes.
- Result table with evaluation command and expected value for each model family.
- Scripted checkpoint download or documented release assets with checksum/version notes.
- Consistent config naming and directory structure.
- README visual mode: model cards plus compact benchmark matrix, not long prose.

Defer:

- Deep explanation of every architecture in the README. Link to docs or papers.

## Inference Demo Or App

Primary promise: users can run the model on an example input quickly.

Prioritize:

- First screen with screenshot, GIF, qualitative grid, or short demo video link.
- One-command local inference path and optional hosted demo link.
- Small sample input assets and expected output directory.
- Clear checkpoint download path and hardware/runtime notes.
- Error messages for missing weights, invalid inputs, and unsupported devices.

Defer:

- Full training refactors if the repo is intentionally inference-only.

## Production ML

Primary promise: users can serve, monitor, or integrate the model reliably.

Prioritize:

- Architecture diagram, serving quickstart, API contract, deployment config, and health checks.
- Deterministic packaging, dependency pinning, container or environment docs.
- Load tests or smoke tests for request/response paths.
- Security notes for user inputs, model files, uploads, secrets, and external services.
- README visual mode: architecture card, endpoint examples, latency/throughput table, and operational limits.

Defer:

- Academic reproduction detail unless the production system also claims paper results.

## Restricted Scientific Or Medical Release

Primary promise: users understand the protocol even when data or weights cannot be fully public.

Prioritize:

- Data access requirements, IRB/license constraints, de-identification notes, and synthetic/demo data path.
- Protocol card: cohort/split definitions, preprocessing, metrics, confidence intervals, and statistical tests.
- Model/data limitations and intended/unsupported use.
- README visuals from diagrams, synthetic data, aggregate plots, or approved anonymized examples.
- Tests using synthetic fixtures, not private data.

Defer:

- Public checkpoint links if sharing is restricted. State access process instead.

## Classification Hints

- If the README starts with paper claims and tables, treat it as a paper release.
- If users are expected to `import package_name`, treat it as a method/library.
- If there are many configs and checkpoints, treat it as a model zoo.
- If the first useful action is uploading or running one image/video/text sample, treat it as a demo/app.
- If there are Docker, service, API, monitoring, or deployment files, check production ML needs.
- If data is human-subject, clinical, biometric, private, or licensed, apply restricted release rules even if another type also fits.
