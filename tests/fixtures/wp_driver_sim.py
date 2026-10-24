"""Deterministic dry-run simulator for the Feature 070 coordination algorithm.

Test-only: nothing here touches the repository or a real line state spine. The
scheduler, verifier, and integrator steps are explicit stubs until their owning
task rows implement them (T018 scheduler, T022 verification/integration), so a
dry run cannot silently pass on unimplemented coordination logic.
"""
from __future__ import annotations

from . import wp_fixtures

# Deterministic fixture graph: two independent read-only packages and one write
# package that depends on the first read-only package.
SIM_READ_A = "plan-wp01"
SIM_READ_B = "plan-wp02"
SIM_WRITE = "plan-wp03"


def sim_packages() -> list:
    read_a = wp_fixtures.make_package(
        SIM_READ_A,
        outputs=["findings/read-a.md"],
        bounded_by={"unit": "tasks", "count": 2},
    )
    read_b = wp_fixtures.make_package(
        SIM_READ_B,
        source_refs=["contracts/scheduler-and-dispatch.md#SD-04"],
        inputs=["contracts/scheduler-and-dispatch.md"],
        outputs=["findings/read-b.md"],
        read_only_paths=["contracts/scheduler-and-dispatch.md"],
        bounded_by={"unit": "tasks", "count": 2},
    )
    write = wp_fixtures.make_write_package(
        SIM_WRITE,
        depends_on=[SIM_READ_A],
        outputs=["src/generated/sim.md"],
        bounded_by={"unit": "tasks", "count": 1},
    )
    return [read_a, read_b, write]


def sim_plan() -> dict:
    return wp_fixtures.make_plan(
        packages=sim_packages(),
        pattern="serial",
        slot_cap=2,
    )


def schedule(plan: dict, **kwargs):
    """SD-01…SD-06 scheduling algorithm (implemented in T018)."""
    raise NotImplementedError(
        "wp_driver_sim.schedule lands with T018 (SD-01…SD-06)"
    )


def verify(plan: dict, results: dict, **kwargs):
    """VI-01…VI-06 independent verification (implemented in T022)."""
    raise NotImplementedError(
        "wp_driver_sim.verify lands with T022 (VI-01…VI-06)"
    )


def integrate(plan: dict, verdicts: dict, **kwargs):
    """VI-07…VI-13 deterministic integration (implemented in T022)."""
    raise NotImplementedError(
        "wp_driver_sim.integrate lands with T022 (VI-07…VI-13)"
    )
