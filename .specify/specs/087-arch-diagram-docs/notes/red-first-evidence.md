# Red-first evidence — 087 arch-diagram-docs (implement stage)

## Evidence landing points (T001)

- notes: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/notes`
- test-evidence: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/test-evidence`

Both are repository paths under `.specify/specs/087-arch-diagram-docs/`; the absolute forms above are the
resolved reading of the same two directories in this worktree. Every row below quotes the command it ran and
the real output it got — nothing here is copied from a planning-phase projection.

Interpreter used for every reading in this file (the one that can `import typer`):

```text
$ /usr/bin/python3 -c "import sys, typer, pytest; print(sys.version); print('typer', typer.__version__); print('pytest', pytest.__version__)"
3.11.13 (main, May 13 2026, 09:30:18) [GCC 10.2.1 20200825 (Alibaba 10.2.1-3.9 2.32)]
typer 0.27.3
pytest 9.2.0
```

(A bare `python3` that cannot `import typer` reports a false red on the mirror checks; see
`notes/pre-change-measurements.md` § T003 for that trap's measured output. It is an environment gap, never
drift.)

