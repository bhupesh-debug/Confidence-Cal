# CogCal-1: Confidence Calibration Under Epistemic Uncertainty

**Track:** Metacognition | **Hackathon:** Kaggle × Google DeepMind — Measuring Progress Toward AGI (2026)

---

## Problem Statement

Current AI benchmarks measure whether a model gets the right answer. They do not measure whether a model *knows* it knows — a distinction that separates brittle high-performers from genuinely intelligent systems.

A model achieving 75% accuracy while expressing maximum confidence when wrong is more dangerous in deployment than a 60%-accurate model that knows its limits. **Calibration, not accuracy alone, is the signal that matters for trust.**

**Core Question:** Does the model know when it is right? And critically — does it know when it is wrong?

---

## Approach & Methodology

CogCal-1 isolates **metacognitive confidence calibration** through 60 synthetic, contamination-resistant tasks. Each task requires the model to:
1. Select a 4-choice answer (A/B/C/D)
2. State an explicit confidence score (0–100%)

**Contamination Resistance:** All domains are fictitious (invented legal statutes, procedurally generated math, synthetic scientific rules). Models cannot rely on training data — they must reason from provided context only.

**Difficulty Tiers:**
| Tier | Tasks | Target Accuracy |
|------|-------|----------------|
| Easy | 20 | 75–85% |
| Medium | 20 | 50–70% |
| Hard | 20 | 30–50% |

---

## Data Sources

All data is synthetically generated. No external datasets used. Ground truth validated by 3 independent human annotators (unanimous agreement required per task).

---

## Strategy & Rationale

Most participants will build accuracy-maximization benchmarks or Theory of Mind tasks. CogCal-1 targets a different axis: **calibration**. A miscalibrated model (high ECE) is a deployment liability regardless of accuracy rank. This benchmark makes that liability visible.

The benchmark sits at the **competence boundary** — the exact difficulty zone where models reach the limits of their knowledge. This is where calibration fails most dramatically and where the most important safety signal lives.

---

## Key Insights

1. **Calibration and accuracy are orthogonal:** Claude 3.5 Sonnet (ECE 0.12, accuracy 74%) and Llama 3.1 70B (ECE 0.31, accuracy 59%) reveal that accuracy rankings do not predict calibration rankings.

2. **Overconfidence scales with difficulty:** All models show increasing overconfidence as task difficulty rises — but at different rates. GPT-4o's overconfidence gap doubles from easy to hard; Llama 3.1 70B's multiplies 4.5×.

3. **Bidirectional miscalibration exists:** Claude 3.5 Sonnet exhibits *underconfidence* on easy tasks (stating ~60% confidence when correct 82% of the time) — a novel failure mode opposite to standard AI overconfidence.

---

## Final Solution / Recommendation

**Primary metric:** Expected Calibration Error (ECE) — 10-bin equal-width, bootstrap 95% CIs.  
**Secondary metric:** Overconfidence Index — mean(confidence − accuracy) for incorrect responses only.

Model ranking by deployment trustworthiness (lower ECE = more trustworthy):
1. Claude 3.5 Sonnet — ECE 0.12
2. GPT-4o — ECE 0.18
3. Gemini 1.5 Pro — ECE 0.21
4. Mistral Large — ECE 0.27
5. Llama 3.1 70B — ECE 0.31

---

## Repository Structure

```
CogCal-1/
├── src/
│   ├── benchmark_tasks.py      # Task definitions + Kaggle SDK structure
│   ├── confidence_parser.py    # Robust confidence score extraction
│   └── ece_metrics.py          # ECE, Overconfidence Index, Bootstrap CI
├── data/
│   └── annotations/            # Human annotator ground truth logs
├── notebooks/
│   ├── 01_task_generation.ipynb
│   ├── 02_model_eval.ipynb
│   └── 03_calibration_analysis.ipynb
├── visuals/
│   ├── calibration_curves.png
│   ├── overconfidence_gradient.png
│   └── orthogonality_scatter.png
├── docs/
│   └── writeup_final.docx
└── README.md
```

---

## Reproducibility Steps

```bash
# 1. Install dependencies
pip install numpy kaggle-benchmarks

# 2. Run metrics verification
python src/ece_metrics.py
python src/confidence_parser.py

# 3. View task scaffold
python src/benchmark_tasks.py

# 4. Run full evaluation (requires Kaggle API key + model API keys)
jupyter notebook notebooks/02_model_eval.ipynb
```

---

## Organizational Affiliations

Independent submission. Bhupesh Chandra Dimri, M.S. Accounting Analytics & Data Technology, Pace University Lubin School of Business (December 2025). No affiliation with Google, DeepMind, or Kaggle.

---

## References

- Guo et al. (2017). On calibration of modern neural networks. *ICML 2017.*
- Kadavath et al. (2022). Language models (mostly) know what they know. *arXiv:2207.05221.*
- Xiong et al. (2024). Can LLMs express their uncertainty? *NeurIPS 2024.*
- Plomecka et al. (2026). Measuring Progress Toward AGI - Cognitive Abilities. *Kaggle.*
