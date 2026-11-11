from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "100a-fixture-alpha"
assert make(".specify/specs/100b-fixture-beta") == "100b-fixture-beta"
