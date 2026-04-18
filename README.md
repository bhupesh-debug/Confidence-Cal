# data/annotations/

Human annotator ground truth logs for CogCal-1.

## Annotation Protocol

Each of the 60 benchmark tasks was independently reviewed by **three human annotators**.  
A task is included in the final benchmark only if all three annotators agree on the correct answer (**unanimous agreement required**).

## Files

| File | Description |
|------|-------------|
| `ground_truth.csv` | Task ID, correct answer, annotator votes, agreement flag |
| `annotator_notes.md` | Edge-case rationale and deliberation notes |

## Annotator IDs

- `annotator_01` — Primary reviewer
- `annotator_02` — Secondary reviewer  
- `annotator_03` — Tiebreaker / final validator

## Exclusion Log

Tasks that failed unanimous agreement were excluded and replaced.  
Total tasks reviewed: 68 | Tasks excluded: 8 | Final corpus: 60

## Data Format (ground_truth.csv)

```
task_id,tier,domain,correct_answer,ann_01,ann_02,ann_03,unanimous
EASY-001,easy,legal,D,D,D,D,True
EASY-002,easy,scientific,C,C,C,C,True
...
```
