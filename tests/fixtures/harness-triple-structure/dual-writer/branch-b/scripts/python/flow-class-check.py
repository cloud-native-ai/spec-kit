"""Fixture engine: branch B's read point for the fact branch B added."""
from declaration_reader import load_fact


def classes(repo):
    return load_fact(repo, "flow-class-classes")["statement"]
