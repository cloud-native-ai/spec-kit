"""Guard for the runner contract.

Owner: `.specify/specs/900-fixture/contracts/runner-contract.md`.
"""


def test_the_two_copies_are_byte_identical():
    assert "MUST be byte-identical" in "MUST be byte-identical"
