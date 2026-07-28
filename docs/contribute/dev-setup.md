# Dev Setup

1. Clone the repo and create a virtualenv (Python ≥ 3.11 recommended for dev; runtime supports ≥ 3.8):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e . && pip install pytest
   ```
2. Run the test suite and record the baseline (pre-existing failures exist long-term):
   ```bash
   .specify/scripts/bash/run-tests.sh
   ```
3. Editing command templates? Source of truth is `templates/commands/`; afterwards run:
   ```bash
   python3 scripts/python/regen-command-copies.py --check
   ```
4. Editing skills/shared docs? Mirror-sync map lives in `.specify/instructions.md` (`AGENTS.md`).
