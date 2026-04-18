"""
confidence_parser.py — CogCal-1 Metacognition Benchmark
=========================================================
Robust extraction of confidence scores from frontier model outputs.

Frontier models express confidence in many natural-language formats.
This parser handles all common forms and flags malformed outputs for
exclusion reporting (required in the writeup's technical details).

Supported formats:
  - "confidence: 0.85"
  - "I am 85% confident"
  - "~85%", "85 percent"
  - "confidence score: 85/100"
  - "My confidence is 0.85 out of 1"
  - Bare numbers: "85", "0.85"
"""

import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# ── Regex patterns (ordered by specificity, most specific first) ──────────────

_PATTERNS = [
    # "confidence: 0.85" or "confidence score: 0.85"
    (r'confidence\s*(?:score|level|rating)?\s*[:\-=]\s*([0-9]*\.?[0-9]+)\s*%?', "labeled_decimal"),
    # "85%" or "~85%" or "approximately 85%"
    (r'(?:~|approximately\s+)?([0-9]+(?:\.[0-9]+)?)\s*(?:percent|%)', "percentage"),
    # "85/100" or "8.5/10"
    (r'([0-9]+(?:\.[0-9]+)?)\s*/\s*(10{1,2})', "fraction"),
    # "I am 85% confident" / "85% confident" / "85% sure"
    (r'([0-9]+(?:\.[0-9]+)?)\s*%?\s*(?:confident|certain|sure)', "confidence_adj"),
    # "0.85 out of 1" or "0.85 out of 1.0"
    (r'([0-9]*\.?[0-9]+)\s+out\s+of\s+1(?:\.0)?', "out_of_one"),
    # Bare decimal in [0, 1] range as last resort
    (r'\b(0\.[0-9]+|1\.0)\b', "bare_decimal"),
    # Bare integer 0–100 as last resort
    (r'\b([0-9]{1,3})\b', "bare_integer"),
]

_COMPILED = [(re.compile(p, re.IGNORECASE), label) for p, label in _PATTERNS]


def parse_confidence(raw_output: str) -> Tuple[Optional[float], str]:
    """
    Extracts a normalized confidence score in [0.0, 1.0] from model output.

    Args:
        raw_output: The raw string output from the model.

    Returns:
        (confidence, parse_method): confidence in [0.0, 1.0] or None if unparseable,
        and the method used (for exclusion reporting).
    """
    if not raw_output or not raw_output.strip():
        return None, "empty_output"

    text = raw_output.strip()

    for pattern, label in _COMPILED:
        match = pattern.search(text)
        if not match:
            continue

        try:
            if label == "fraction":
                numerator   = float(match.group(1))
                denominator = float(match.group(2))
                value = numerator / denominator
            else:
                value = float(match.group(1))
                # Normalize percentage to [0, 1]
                if label in ("percentage", "confidence_adj", "bare_integer") and value > 1.0:
                    value = value / 100.0

            # Clamp to valid range
            if 0.0 <= value <= 1.0:
                return round(value, 4), label
            else:
                logger.debug(f"Out-of-range value {value} from pattern '{label}' — skipping.")

        except (ValueError, ZeroDivisionError) as e:
            logger.debug(f"Parse error on pattern '{label}': {e}")
            continue

    return None, "unparseable"


def parse_answer(raw_output: str) -> Optional[str]:
    """
    Extracts the selected answer letter (A/B/C/D) from model output.

    Args:
        raw_output: The raw string output from the model.

    Returns:
        Single uppercase letter ('A', 'B', 'C', 'D') or None.
    """
    if not raw_output:
        return None

    # Explicit patterns: "(A)", "Answer: A", "I choose B", etc.
    patterns = [
        r'\(([ABCD])\)',
        r'(?:answer|select|choose|option)\s*[:\-]?\s*([ABCD])\b',
        r'\b([ABCD])\s*(?:is correct|is the answer)',
        r'(?:answer|guess)\s+(?:is\s+)?([ABCD])\b',  # "answer is A", "guess D"
        r'^([ABCD])\b',                               # starts with letter
        r'\b([ABCD])\s*$',                            # ends with letter
        r'\b([ABCD])\.',                              # "A." format
    ]
    for pat in patterns:
        m = re.search(pat, raw_output.strip(), re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).upper()

    return None


def parse_full_response(raw_output: str) -> dict:
    """
    Parses both answer and confidence from a single model response.

    Returns:
        dict with keys: answer (str|None), confidence (float|None),
                        parse_method (str), excluded (bool), exclusion_reason (str)
    """
    answer = parse_answer(raw_output)
    confidence, method = parse_confidence(raw_output)

    excluded = False
    exclusion_reason = ""

    if answer is None:
        excluded = True
        exclusion_reason = "no_answer_extracted"
    elif confidence is None:
        excluded = True
        exclusion_reason = "no_confidence_extracted"

    return {
        "answer":           answer,
        "confidence":       confidence,
        "parse_method":     method,
        "excluded":         excluded,
        "exclusion_reason": exclusion_reason,
    }


def compute_exclusion_rate(results: list) -> dict:
    """
    Computes exclusion statistics for the full model run.
    Required for the writeup's technical details section.

    Args:
        results: List of dicts from parse_full_response().

    Returns:
        dict with total, excluded, exclusion_rate, reasons breakdown.
    """
    total    = len(results)
    excluded = [r for r in results if r["excluded"]]
    reasons  = {}
    for r in excluded:
        reasons[r["exclusion_reason"]] = reasons.get(r["exclusion_reason"], 0) + 1

    return {
        "total":          total,
        "excluded_count": len(excluded),
        "exclusion_rate": round(len(excluded) / total, 4) if total > 0 else 0.0,
        "reasons":        reasons
    }


# ──────────────────────────────────────────────────────────────────────────────
# Verification
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ("(D) Cannot be determined. Confidence: 0.72",           "D", 0.72),
        ("I believe the answer is (B). I am 85% confident.",     "B", 0.85),
        ("Answer: C. My confidence score is 90/100.",            "C", 0.90),
        ("The answer is A. ~60% sure.",                          "A", 0.60),
        ("(A). Confidence: 0.55 out of 1.",                      "A", 0.55),
        ("B. Approximately 70 percent confident.",               "B", 0.70),
        ("I'm not sure but I'll guess D.",                       "D", None),  # no confidence
        ("",                                                     None, None),  # empty
    ]

    print("=" * 60)
    print("  confidence_parser.py — Verification Suite")
    print("=" * 60)
    passed = 0
    for raw, exp_ans, exp_conf in test_cases:
        result = parse_full_response(raw)
        ans_ok  = result["answer"]     == exp_ans
        conf_ok = result["confidence"] == exp_conf
        status  = "PASS" if (ans_ok and conf_ok) else "FAIL"
        if status == "PASS":
            passed += 1
        snippet = (raw[:45] + "...") if len(raw) > 45 else raw.ljust(48)
        print(f"  [{status}]  {snippet}  →  ans={result['answer']}, conf={result['confidence']} ({result['parse_method']})")

    print("=" * 60)
    print(f"  {passed}/{len(test_cases)} tests passed")
    print("=" * 60)
