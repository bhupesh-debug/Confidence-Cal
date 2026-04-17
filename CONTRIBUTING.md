# Contributing to CogCal-1

Thank you for your interest in contributing to CogCal-1.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs in task definitions, metric implementations, or parser edge cases
- Include a minimal reproducible example where applicable

### Proposing New Tasks
- Follow the task construction guide in `docs/task_construction_guide.md`
- Submit tasks with a completed `CogCalTask` dataclass entry including rationale and at least one annotator review
- Open a pull request targeting the `dev` branch

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Write tests for any new functions in `tests/`
4. Ensure all tests pass: `pytest tests/ -v`
5. Open a pull request with a clear description

## Code Style
- Follow PEP 8
- Docstrings on all public functions (Google style)
- Type annotations required for function signatures

## Questions
Open a GitHub Issue with the `question` label.
