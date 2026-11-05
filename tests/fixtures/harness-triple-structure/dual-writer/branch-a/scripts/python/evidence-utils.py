"""Fixture engine: branch A's read point for the fact branch A added."""
from declaration_reader import load_fact


def states(repo):
    return load_fact(repo, "evidence-seven-states")["statement"]
