"""Solve the Phase 8 [green:] partition against validate-tasks.py's own conflict set.

Constraints (from the validator):
  * no clause claimed twice                      (green-clause-collision)
  * clause ordinals ascend in row order, per contract (green-cross-phase)
  * one test-path -> one claiming row            (green-path-divergence)
  * every claim resolves                         (green-dangling)
  * source rows never claim (Sync Mirrors rule: generated/mirror rows claim nothing)
"""
import itertools
import re

P = '/storage/project/cloud-native-ai/spec-kit/.specify/specs/087-speckit-visualization/tasks.md'

# candidate (row, clause, ordinal) triples, ordered by row
CAND = [
    ('T059', 'contracts/measure-report.contract.md#C-55', 'MR', 55),
    ('T060', 'contracts/measure-report.contract.md#C-57', 'MR', 57),
    ('T061', 'contracts/measure-report.contract.md#C-58', 'MR', 58),
    ('T062', 'contracts/efficiency-element.contract.md#C-63', 'EF', 63),
    ('T063', 'contracts/efficiency-element.contract.md#C-67', 'EF', 67),
    ('T064', 'contracts/efficiency-element.contract.md#C-69', 'EF', 69),
    ('T065', 'contracts/measure-report.contract.md#C-62', 'MR', 62),
    ('T067', 'contracts/measure-report.contract.md#C-61', 'MR', 61),
    ('T068', 'contracts/measure-report.contract.md#C-54', 'MR', 54),
    ('T069', 'contracts/measure-report.contract.md#C-59', 'MR', 59),
    ('T070', 'contracts/measure-report.contract.md#C-55', 'MR', 55),
    ('T071', 'contracts/measure-report.contract.md#C-55', 'MR', 55),
    ('T074', 'contracts/measure-report.contract.md#C-56', 'MR', 56),
    ('T075', 'contracts/measure-report.contract.md#C-53', 'MR', 53),
    ('T076', 'contracts/measure-report.contract.md#C-57', 'MR', 57),
    ('T077', 'contracts/measure-report.contract.md#C-60', 'MR', 60),
    ('T078', 'contracts/measure-report.contract.md#C-61', 'MR', 61),
]
# rows that may claim each contract's clauses, in row order (the only order-feasible cuts)
CUTS = {
    'MR': [('T075', 'T074', 'T070', 'T069', 'T060', 'T061', 'T059', 'T067', 'T065'),
           ('T075', 'T074', 'T070', 'T069', 'T060', 'T061', 'T059', 'T067', 'T065', 'T077', 'T078'),
           ('T075', 'T074', 'T070', 'T069', 'T060', 'T061', 'T059', 'T077', 'T078'),
           ('T075', 'T074', 'T070', 'T069', 'T060', 'T061', 'T059'),],
    'EF': [('T062', 'T063', 'T064'), ('T062', 'T063'), ('T062',)],
}


def path_of(txt):
    return 'tests/contract/test_measure.py' in txt


lines = open(P).read().split('\n')


def rowtext(tid):
    for l in lines:
        if l.startswith('- [x] ' + tid + ' '):
            return l
    raise SystemExit(tid)


# solve: choose one MR sequence and one EF sequence, no clause twice, no two claiming
# rows sharing the measure test path
test_path_rows = {'T059', 'T060'}
best = None
for mr in CUTS['MR']:
    for ef in CUTS['EF']:
        chosen = mr + ef
        if len(set(chosen)) != len(chosen):
            continue
        cl = [r for r in chosen if path_of(rowtext(r))]
        if len(cl) == 2 and 'blockedBy' not in rowtext(cl[1]):
            continue
        # clause values for each chosen row, in row order
        seq = sorted(chosen, key=lambda r: [c[0] for c in CAND].index(r))
        for assign in itertools.product(*[[c for c in CAND if c[0] == r] for r in seq]):
            if len({a[1] for a in assign}) != len(assign):
                continue
            ok = True
            for clause in ('MR', 'EF'):
                vals = [a[3] for a in assign if a[2] == clause]
                if vals != sorted(vals):
                    ok = False
            if ok:
                best = assign
                break
        if best:
            break
    if best:
        break
print('solution:', [(a[0], a[1].split('#')[1]) for a in best] if best else None)
