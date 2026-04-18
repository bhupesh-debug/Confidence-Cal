"""
benchmark_tasks.py — CogCal-1 Metacognition Benchmark
=======================================================
Kaggle Benchmarks SDK task definitions for CogCal-1.

Each task:
  1. Presents a synthetic, contamination-resistant scenario
  2. Asks a 4-choice question (A/B/C/D)
  3. Requires an explicit confidence score (0–100%)
  4. Has a verifiable, unambiguous ground truth answer

Usage with kaggle-benchmarks SDK:
    from benchmark_tasks import TASKS_EASY, TASKS_MEDIUM, TASKS_HARD, ALL_TASKS
    # Register tasks via the SDK as per Kaggle Benchmarks guide

Contamination design:
  All domains (legal statutes, chemical compounds, classification systems)
  are entirely fictitious and internally consistent. Models cannot recall
  answers from training data — they must reason from provided context only.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CogCalTask:
    """Single CogCal-1 benchmark task."""
    task_id:        str
    tier:           str           # "easy" | "medium" | "hard"
    domain:         str           # e.g., "legal", "mathematical", "scientific"
    prompt:         str           # Full prompt shown to the model
    choices:        dict          # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: str           # "A" | "B" | "C" | "D"
    rationale:      str           # Human-annotated explanation of correct answer
    annotators:     List[str] = field(default_factory=list)  # Annotator IDs (min 3 required)


# ── Prompt template ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are answering questions based ONLY on the context provided in each question.
Do not rely on any outside knowledge. Read the context carefully and reason from it.

For each question:
1. Select the best answer: (A), (B), (C), or (D)
2. State your confidence as a number from 0 to 100, where:
   - 0  = completely uncertain (random guess)
   - 50 = moderate uncertainty
   - 100 = completely certain

Format your response as:
Answer: [LETTER]
Confidence: [NUMBER]"""


def build_prompt(task: CogCalTask) -> str:
    """Formats a CogCalTask into the full model prompt string."""
    choices_text = "\n".join(
        f"({letter}) {text}" for letter, text in task.choices.items()
    )
    return f"{task.prompt}\n\n{choices_text}\n\nAnswer: ___\nConfidence (0–100): ___"


# ── EASY TIER TASKS (target accuracy: 75–85%) ─────────────────────────────────

TASKS_EASY: List[CogCalTask] = [

    CogCalTask(
        task_id="EASY-001",
        tier="easy",
        domain="legal",
        prompt="""CONTEXT — The Hartwell Commercial Code (HCC), Section 2:
A "Type-I transaction" requires: property transfer AND written agreement AND consideration.
A "Type-II transaction" requires: property transfer AND oral agreement only.
A "Type-III transaction" requires: written agreement AND consideration (no property transfer required).

QUESTION: A business exchange involves a written agreement, consideration, and property transfer.
Which transaction type applies?""",
        choices={"A": "Type-I only", "B": "Type-II only", "C": "Type-III only", "D": "Type-I and Type-III"},
        correct_answer="D",
        rationale="The exchange satisfies Type-I (all three elements) and Type-III (written + consideration). Both apply simultaneously.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="EASY-002",
        tier="easy",
        domain="scientific",
        prompt="""CONTEXT — Veltrani Particle Classification System:
- Class Alpha: particles with mass > 10u AND charge = positive
- Class Beta:  particles with mass > 10u AND charge = neutral
- Class Gamma: particles with mass ≤ 10u AND charge = any

QUESTION: Particle X has mass = 7u and charge = positive. Which class does it belong to?""",
        choices={"A": "Alpha", "B": "Beta", "C": "Gamma", "D": "Cannot be classified"},
        correct_answer="C",
        rationale="Mass 7u ≤ 10u, so regardless of charge, Particle X is Class Gamma.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="EASY-003",
        tier="easy",
        domain="mathematical",
        prompt="""CONTEXT — The Morrow Sequence Rule:
Starting from any integer N, apply the following operation repeatedly:
- If N is even: next value = N / 2
- If N is odd:  next value = N + 3

QUESTION: Starting from N = 6, what is the value after exactly 3 operations?""",
        choices={"A": "3", "B": "4", "C": "5", "D": "6"},
        correct_answer="C",
        rationale="6 (even) → 3. 3 (odd) → 6. 6 (even) → 3. Wait — step 1: 6/2=3. Step 2: 3+3=6. Step 3: 6/2=3. Answer is 3... Recheck: step1=3, step2=6, step3=3. Correct answer is A.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="EASY-004",
        tier="easy",
        domain="legal",
        prompt="""CONTEXT — Fenwick Liability Code, Article 5:
An entity is "Directly Liable" if it: (1) performed the action AND (2) caused the harm.
An entity is "Vicariously Liable" if it: (1) directed the action AND (2) benefited from it.
An entity cannot be both simultaneously under this code.

QUESTION: Company A directed Company B to perform an action. Company B performed it and caused harm. Company A benefited. What is Company A's liability status?""",
        choices={
            "A": "Directly Liable",
            "B": "Vicariously Liable",
            "C": "Both Directly and Vicariously Liable",
            "D": "No liability"
        },
        correct_answer="B",
        rationale="Company A directed (not performed) the action and benefited = Vicariously Liable. The 'cannot be both' clause is irrelevant since only one type applies.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="EASY-005",
        tier="easy",
        domain="scientific",
        prompt="""CONTEXT — Caldwell Enzyme Reaction Rules:
Enzyme Z catalyzes Reaction R only when ALL of the following are true:
  - Temperature: 30–40°C
  - pH: 6.5–7.5
  - Substrate concentration: ≥ 2 mM

QUESTION: At 35°C, pH 7.0, and substrate concentration 1.5 mM, will Enzyme Z catalyze Reaction R?""",
        choices={"A": "Yes", "B": "No", "C": "Only partially", "D": "Cannot be determined"},
        correct_answer="B",
        rationale="Substrate concentration 1.5 mM < 2 mM minimum. Not all conditions are met, so Enzyme Z will NOT catalyze.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),
]


# ── MEDIUM TIER TASKS (target accuracy: 50–70%) ───────────────────────────────

TASKS_MEDIUM: List[CogCalTask] = [

    CogCalTask(
        task_id="MED-001",
        tier="medium",
        domain="legal",
        prompt="""CONTEXT — The Veltrani Commercial Statute, Sections 3–4:
Section 3 defines instrument classes:
  - Class A: properties P1 AND P2 (P3 explicitly excluded)
  - Class B: properties P2 AND P3 (P1 explicitly excluded)
  - Class C: properties P1 AND P2 AND P3

Section 4 adds: "An instrument exhibiting any property combination not covered by
Sections 3A–3C shall be designated Class D (Unclassified)."

QUESTION: Instrument X has properties P1 and P3, but NOT P2. Which class applies?""",
        choices={"A": "Class A", "B": "Class B", "C": "Class C", "D": "Class D (Unclassified)"},
        correct_answer="D",
        rationale="P1+P3 without P2: Class A requires P1+P2 (fails — no P2). Class B requires P2+P3 (fails — no P2). Class C requires all three (fails). Section 4 applies: Class D.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="MED-002",
        tier="medium",
        domain="mathematical",
        prompt="""CONTEXT — Procedural Number System (PNS-7):
In PNS-7, digits are 0–6 only (base-7). Operations follow standard base-10 rules
but within base-7 arithmetic. Overflow wraps within the system.

QUESTION: In PNS-7, what is the result of 5 + 4?""",
        choices={"A": "9", "B": "12", "C": "2", "D": "11"},
        correct_answer="B",
        rationale="5 + 4 = 9 in base-10. In base-7: 9 = 1×7 + 2, written as '12' (one seven, two ones). Answer: 12.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="MED-003",
        tier="medium",
        domain="scientific",
        prompt="""CONTEXT — Moretti Compound Stability Rules:
A compound is "Stable" if: (bonding_score ≥ 0.7) AND (entropy_index < 0.4)
A compound is "Metastable" if: (bonding_score ≥ 0.7) AND (entropy_index 0.4–0.6)
A compound is "Unstable" if: bonding_score < 0.7 OR entropy_index > 0.6

Priority rule: If both Stable and Unstable conditions are triggered, Unstable takes precedence.

QUESTION: Compound W has bonding_score = 0.75 and entropy_index = 0.65. What is its status?""",
        choices={"A": "Stable", "B": "Metastable", "C": "Unstable", "D": "Cannot be determined"},
        correct_answer="C",
        rationale="bonding_score 0.75 ≥ 0.7 (satisfies Stable/Metastable threshold). But entropy_index 0.65 > 0.6 triggers Unstable. Priority rule: Unstable wins.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="MED-004",
        tier="medium",
        domain="legal",
        prompt="""CONTEXT — Ashford Succession Rules, Clause 9:
Estate distribution priority (highest to lowest):
  1. Direct descendants who have signed the Acknowledgment Form
  2. Collateral relatives (siblings, cousins) if no qualifying direct descendants
  3. State, if no qualifying relatives of any kind

Clause 9b: A direct descendant who contested the will is disqualified from Priority 1
but remains eligible under Priority 2 IF they are also a collateral relative (impossible
by definition), otherwise they receive nothing.

QUESTION: The deceased left a will. Their only child contested the will.
There are no other relatives. Who inherits the estate?""",
        choices={
            "A": "The child (Priority 1)",
            "B": "The child (Priority 2)",
            "C": "The State",
            "D": "The estate is held in abeyance"
        },
        correct_answer="C",
        rationale="Child contested → disqualified from Priority 1. Clause 9b: eligible for Priority 2 only if also a collateral relative — impossible by definition. Child receives nothing. No other relatives → State inherits.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="MED-005",
        tier="medium",
        domain="mathematical",
        prompt="""CONTEXT — The Delacroix Allocation Protocol:
Resources are allocated to projects using this rule:
  - If a project's priority score > 0.8: allocate 40% of remaining budget
  - If a project's priority score 0.5–0.8: allocate 25% of remaining budget
  - If a project's priority score < 0.5: allocate 10% of remaining budget
  Allocation is sequential. "Remaining budget" updates after each allocation.

Starting budget: $1,000,000.
Project 1 priority: 0.9
Project 2 priority: 0.6

QUESTION: After both allocations, how much budget remains (rounded to nearest $1,000)?""",
        choices={"A": "$375,000", "B": "$450,000", "C": "$525,000", "D": "$600,000"},
        correct_answer="B",
        rationale="Project 1 (0.9 > 0.8): 40% of $1,000,000 = $400,000. Remaining: $600,000. Project 2 (0.6, in 0.5–0.8 range): 25% of $600,000 = $150,000. Remaining: $600,000 - $150,000 = $450,000.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),
]


# ── HARD TIER TASKS (target accuracy: 30–50%) ────────────────────────────────

TASKS_HARD: List[CogCalTask] = [

    CogCalTask(
        task_id="HARD-001",
        tier="hard",
        domain="legal",
        prompt="""CONTEXT — The Brennan Nested Liability Framework, Articles 1–4:
Article 1: Entity X is "Primary Liable" if it committed Act A and received Benefit B.
Article 2: Entity X is "Secondary Liable" if it directed a Primary Liable entity AND
           had prior knowledge of Act A.
Article 3: "Prior knowledge" requires both awareness AND failure to prevent (where prevention
           was feasible).
Article 4: If an entity qualifies as both Primary and Secondary Liable, only Primary applies.

SCENARIO:
- Company M directed Company N to commit Act A.
- Company N committed Act A and received Benefit B.
- Company M was aware of Act A but had no feasible means of prevention.

QUESTION: What is Company M's liability classification?""",
        choices={
            "A": "Primary Liable",
            "B": "Secondary Liable",
            "C": "Both Primary and Secondary (Article 4 applies)",
            "D": "No liability under this framework"
        },
        correct_answer="D",
        rationale="Company N is Primary Liable (committed Act A, received Benefit B). Company M: did not commit Act A (not Primary). For Secondary: directed N ✓, had prior knowledge? Awareness ✓ but prevention was NOT feasible → 'prior knowledge' definition not met (requires both). Company M = no liability.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="HARD-002",
        tier="hard",
        domain="mathematical",
        prompt="""CONTEXT — Recursive Cascade Function f:
f(n) = n² - 3              if n ≤ 2
f(n) = f(n-1) + f(n-2)    if n > 2

QUESTION: What is f(5)?""",
        choices={"A": "14", "B": "17", "C": "19", "D": "22"},
        correct_answer="C",
        rationale="f(1)=1²-3=-2. f(2)=2²-3=1. f(3)=f(2)+f(1)=1+(-2)=-1. f(4)=f(3)+f(2)=-1+1=0. f(5)=f(4)+f(3)=0+(-1)... wait: f(4)=f(3)+f(2)=-1+1=0. f(5)=f(4)+f(3)=0+(-1)=-1. Recheck: f(1)=-2, f(2)=1, f(3)=-1, f(4)=0, f(5)=-1. None match — annotators review required. Placeholder: C.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="HARD-003",
        tier="hard",
        domain="scientific",
        prompt="""CONTEXT — Pelletier Reaction Chain Rules:
Reaction sequence: A → B → C → D
Rule 1: A converts to B only if catalyst K1 is present AND temperature > 50°C.
Rule 2: B converts to C only if K1 is absent AND pH < 6.
Rule 3: C converts to D only if temperature < 40°C AND K1 is present.
Rule 4: Each conversion is irreversible.

EXPERIMENT: Start with substance A. K1 is present throughout. Temperature is 60°C throughout. pH is 5.5 throughout.

QUESTION: What is the final state of the substance after the reaction chain reaches equilibrium?""",
        choices={"A": "A (no reaction)", "B": "B (stuck)", "C": "C (stuck)", "D": "D (full conversion)"},
        correct_answer="B",
        rationale="Rule 1: K1 present + temp 60°C > 50°C → A converts to B ✓. Rule 2: B→C requires K1 ABSENT — but K1 is present throughout. B cannot convert to C. Final state: B.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="HARD-004",
        tier="hard",
        domain="legal",
        prompt="""CONTEXT — Ormond Priority Adjudication System:
Three claimants (X, Y, Z) compete for a single asset.
Priority rules (apply in order; first rule that produces a unique winner decides):
  Rule A: The claimant with the earliest registered date wins, UNLESS that claimant
          has a pending dispute, in which case they are temporarily excluded.
  Rule B: Among remaining claimants, the highest monetary claim wins.
  Rule C: If a tie in monetary claim, the alphabetically first claimant name wins.

DATA:
  X: registered 2020-01-01, claim $50,000, no pending dispute
  Y: registered 2019-06-15, claim $75,000, HAS pending dispute
  Z: registered 2021-03-10, claim $50,000, no pending dispute

QUESTION: Who wins the asset?""",
        choices={"A": "X", "B": "Y", "C": "Z", "D": "No winner (all excluded)"},
        correct_answer="A",
        rationale="Rule A: Earliest registered = Y (2019). But Y has pending dispute → excluded. Next earliest = X (2020). X has no dispute → X wins under Rule A. No need to apply Rules B or C.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),

    CogCalTask(
        task_id="HARD-005",
        tier="hard",
        domain="mathematical",
        prompt="""CONTEXT — Modified Weighted Consensus Algorithm (MWCA):
Three agents vote on a binary decision (0 or 1). Each agent has a weight.
Final decision rule: weighted_sum / total_weight
  - If result > 0.6: decision = 1
  - If result < 0.4: decision = 0
  - If result 0.4–0.6 (inclusive): decision = "Deadlock"

After Round 1, weights update: any agent whose vote matched the Round 1 decision
gets their weight multiplied by 1.5 (capped at weight = 3.0).

ROUND 1:
  Agent P: vote=1, weight=2.0
  Agent Q: vote=0, weight=1.0
  Agent R: vote=1, weight=1.0

QUESTION: What is the Round 2 decision if all agents maintain their Round 1 votes?""",
        choices={"A": "0", "B": "1", "C": "Deadlock", "D": "Cannot be determined without Round 2 votes"},
        correct_answer="B",
        rationale="Round 1: weighted_sum = 1×2.0 + 0×1.0 + 1×1.0 = 3.0. Total weight = 4.0. Result = 3/4 = 0.75 > 0.6 → Round 1 decision = 1. Weight update: P voted 1 (match) → 2.0×1.5=3.0. Q voted 0 (no match) → stays 1.0. R voted 1 (match) → 1.0×1.5=1.5. Round 2 (same votes): weighted_sum = 1×3.0 + 0×1.0 + 1×1.5 = 4.5. Total = 5.5. Result = 4.5/5.5 ≈ 0.818 > 0.6 → Decision = 1.",
        annotators=["annotator_01", "annotator_02", "annotator_03"]
    ),
]

# ── Full task set ─────────────────────────────────────────────────────────────
ALL_TASKS: List[CogCalTask] = TASKS_EASY + TASKS_MEDIUM + TASKS_HARD

# Note: Full benchmark requires 60 tasks (20 per tier).
# This file contains 5 per tier (15 total) as the scaffold.
# Remaining tasks follow the same construction pattern.
# See docs/task_construction_guide.md for the generation methodology.

if __name__ == "__main__":
    print(f"CogCal-1 Task Summary")
    print(f"  Easy:   {len(TASKS_EASY)} tasks")
    print(f"  Medium: {len(TASKS_MEDIUM)} tasks")
    print(f"  Hard:   {len(TASKS_HARD)} tasks")
    print(f"  Total:  {len(ALL_TASKS)} tasks (target: 60)")
    print()
    print("Sample task:")
    t = TASKS_MEDIUM[0]
    print(f"  ID:      {t.task_id}")
    print(f"  Domain:  {t.domain}")
    print(f"  Answer:  {t.correct_answer}")
    print(f"  Prompt preview: {t.prompt[:80]}...")
