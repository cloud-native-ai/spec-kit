"""Fixture engine: keeps its inline constant — no read point, so the unit stays pending."""
THRESHOLD = 10


def threshold():
    return THRESHOLD
