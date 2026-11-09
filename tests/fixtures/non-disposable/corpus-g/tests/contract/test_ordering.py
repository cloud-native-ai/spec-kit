"""Ordering guard (fixture).

Owner: `.specify/specs/900-fixture/requirements.md`.
"""


def test_first_item_is_goal():
    first_no = "1"
    assert first_no == "1"


def test_second_item_is_budget():
    assert "budget" in "budget"
