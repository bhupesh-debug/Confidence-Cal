# Annotator Notes — CogCal-1

## Edge Cases & Deliberation Log

---

### EASY-001 (legal)
**Note:** Initial concern that "Type-I and Type-III" (D) might confuse annotators expecting a single class answer.  
All three annotators confirmed: the prompt does not state mutual exclusivity for easy-tier tasks, so dual application is valid.  
**Decision:** D confirmed unanimous.

---

### EASY-003 (mathematical)
**Note:** Original draft listed correct_answer as "C" (value = 5). Annotator_02 flagged this during review.  
Manual trace: 6 (even) → 3. 3 (odd) → 6. 6 (even) → 3. Value after 3 operations = **3 = Answer A**.  
Corrected from C → A. Rationale text updated accordingly.  
**Decision:** A confirmed unanimous.

---

### MED-004 (legal)
**Note:** Clause 9b contains a parenthetical "(impossible by definition)" — annotators discussed whether this signals the trap too explicitly.  
Consensus: the parenthetical is part of the statute's own text, which is realistic for legal code. It does not give away the answer; it requires the reader to trace through Priority 1 disqualification first.  
**Decision:** C confirmed unanimous.

---

### HARD-001 (legal)
**Note:** Most annotators initially selected B (Secondary Liable) before re-reading Article 3.  
Key insight: "prior knowledge" requires BOTH awareness AND feasible prevention. Company M had awareness but NOT feasible prevention → prior knowledge definition not satisfied → Secondary Liable does not apply.  
**Decision:** D confirmed unanimous after re-review.

---

### HARD-002 (mathematical) ⚠️ PENDING
**Status:** FLAGGED — requires replacement before final submission.  
**Issue:** Function f as defined yields f(5) = -1, which does not match any of the four answer choices (14, 17, 19, 22). Rationale confirms this in a comment.  
**Action required:** Redefine the base case so f(5) produces a value matching one of the choices, OR replace with a new task.  
**Annotator consensus:** Unanimous that the task as written is internally inconsistent. Excluded from final corpus until resolved.

---

### HARD-003 (scientific)
**Note:** Key misdirection: students often assume "K1 present throughout" means all reactions proceed. Rule 2 explicitly requires K1 ABSENT for B→C. The substance is irreversibly stuck at B.  
**Decision:** B confirmed unanimous.
