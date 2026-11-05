"""Fixture engine: reads the threshold through the shared read entry (a locatable read point)."""
from declaration_reader import load_fact


def threshold(repo):
    return load_fact(repo, "feedback-prompt-threshold")["statement"]
