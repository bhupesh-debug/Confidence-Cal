"""
CogCal-1: Confidence Calibration Under Epistemic Uncertainty
============================================================
A metacognition benchmark for frontier language models.

Modules:
    benchmark_tasks     — Task definitions (60 synthetic MCQ tasks, 3 tiers)
    confidence_parser   — Robust confidence score extraction from model outputs
    ece_metrics         — ECE, Overconfidence Index, Bootstrap CI computation

Track: Metacognition | Kaggle × Google DeepMind — Measuring Progress Toward AGI (2026)
Author: Bhupesh Chandra Dimri, Pace University Lubin School of Business
"""

from .ece_metrics import calculate_ece, calculate_overconfidence_index, bootstrap_ece_ci, full_calibration_report
from .confidence_parser import parse_confidence, parse_answer, parse_full_response
from .benchmark_tasks import ALL_TASKS, TASKS_EASY, TASKS_MEDIUM, TASKS_HARD, CogCalTask

__version__ = "1.0.0"
__author__ = "Bhupesh Chandra Dimri"
