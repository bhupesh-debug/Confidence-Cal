# Changelog

All notable changes to CogCal-1 are documented here.

## [1.0.0] — 2026-04-16
### Initial Submission — Kaggle × Google DeepMind AGI Hackathon 2026

**Added**
- 15-task scaffold (5 per tier) with full `CogCalTask` dataclass definitions
- `ece_metrics.py`: ECE, Overconfidence Index, Bootstrap 95% CI
- `confidence_parser.py`: Multi-pattern regex confidence extractor with exclusion reporting
- `benchmark_tasks.py`: Task definitions + Kaggle SDK structure + `SYSTEM_PROMPT`
- `tests/`: pytest suites for ECE metrics and confidence parser
- `.github/workflows/ci.yml`: GitHub Actions CI across Python 3.10 and 3.11
- `docs/task_construction_guide.md`: Full methodology for task authoring
- `data/annotations/`: Ground truth CSV + annotator deliberation notes

**Known Issues**
- HARD-002: Task answer choices do not match computed f(5). Flagged in annotator notes. Replacement task in progress.
- Task corpus is 15/60 scaffold. Full 60-task corpus to be added in v1.1.0.

## [1.1.0] — Planned
- Complete 60-task corpus (20 per tier)
- HARD-002 replacement
- Full calibration curve visualizations
- Model evaluation notebooks (02_model_eval.ipynb)
