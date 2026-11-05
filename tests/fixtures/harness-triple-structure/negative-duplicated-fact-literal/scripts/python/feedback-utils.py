"""Fixture engine: reads the threshold through the shared read entry."""
from declaration_reader import load_fact


def threshold(repo):
    return load_fact(repo, "feedback-prompt-threshold")["statement"]
