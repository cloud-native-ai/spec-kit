from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "record-retention.py"


def _load():
    name = "_test_record_retention"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_iso_accepts_z_and_offsets():
    engine = _load()
    assert engine.parse_iso("2026-09-01T00:00:00Z") is not None
    assert engine.parse_iso("2026-09-01T08:00:00+08:00") is not None
    assert engine.parse_iso("") is None
    assert engine.parse_iso("not-a-date") is None


def test_age_days_is_positive_for_old_and_none_for_unparseable():
    engine = _load()
    assert engine.age_days("2026-09-01T00:00:00Z") > 0
    assert engine.age_days("") is None
    assert engine.age_days("not-a-date") is None


def test_selected_stores_all_and_unknown():
    engine = _load()
    assert engine.selected_stores("all") == list(engine.STORES)
    assert engine.selected_stores("exec-quant,feedback") == ["exec-quant", "feedback"]
    try:
        engine.selected_stores("nope")
    except engine.RetentionError:
        pass
    else:
        raise AssertionError("unknown store must be rejected")


def test_entry_hash_is_store_qualified_and_stable():
    engine = _load()
    a = engine.entry_hash("feedback", "same")
    b = engine.entry_hash("feedback", "same")
    c = engine.entry_hash("session-note", "same")
    assert a == b
    assert a != c
    assert len(a) == 12
