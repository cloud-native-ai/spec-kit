"""Registry, routing and command-line contract for database-utils (MIT rewrite).

Covers the parts of the interface a caller meets before any server is contacted:
where the connection file is looked up, what a missing or malformed entry prints,
how a protocol is resolved, how a handler is loaded, and which mode wins on the
command line. The dispatcher's routing is exercised against a recording stub, so
these cases need neither a driver nor a database.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "external" / "database-utils"
SCRIPTS = SKILL / "scripts"

ENTRY = {
    "name": "shop",
    "description": "orders, customers",
    "host": "db.internal",
    "port": 3306,
    "database": "shop",
    "user": "reader",
    "password": "secret",
}


def _load(script_name: str, module_name: str):
    path = SCRIPTS / script_name
    assert path.is_file(), f"script missing: {path}"
    saved_path, saved_argv = list(sys.path), list(sys.argv)
    sys.argv = [str(path)]
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.argv = saved_argv
        sys.path[:] = saved_path
    return module


@pytest.fixture(scope="module")
def dispatcher():
    return _load("query.py", "_dbutils_dispatcher_cfg")


@pytest.fixture(scope="module")
def mysql():
    return _load("query_mysql.py", "_dbutils_mysql_cfg")


@pytest.fixture(scope="module")
def postgres():
    return _load("query_postgres.py", "_dbutils_postgres_cfg")


@pytest.fixture
def registry(tmp_path):
    """A readable-only-by-owner registry file holding one entry."""
    path = tmp_path / "connections.json"
    path.write_text(json.dumps({"databases": [dict(ENTRY)]}), encoding="utf-8")
    path.chmod(0o600)
    return path


# --------------------------------------------------------------------------- #
# Lookup order
# --------------------------------------------------------------------------- #
def test_dispatcher_search_order(dispatcher):
    assert dispatcher.CONFIG_LOCATIONS == [
        dispatcher.SKILL_DIR / "connections.json",
        Path.home() / ".config" / "claude" / "db-connections.json",
    ]
    assert dispatcher.SCRIPT_DIR == SCRIPTS
    assert dispatcher.SKILL_DIR == SKILL


@pytest.mark.parametrize("handler_name,leaf", [
    ("mysql", "mysql-connections.json"),
    ("postgres", "postgres-connections.json"),
])
def test_handler_search_order(request, handler_name, leaf):
    handler = request.getfixturevalue(handler_name)
    assert handler.CONFIG_LOCATIONS == [
        SKILL / "connections.json",
        Path.home() / ".config" / "claude" / leaf,
    ]


def test_first_existing_candidate_wins(dispatcher, tmp_path, monkeypatch):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    second.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(dispatcher, "CONFIG_LOCATIONS", [first, second])
    assert dispatcher.find_config() == second
    first.write_text("{}", encoding="utf-8")
    assert dispatcher.find_config() == first


def test_no_candidate_returns_none(dispatcher, tmp_path, monkeypatch):
    monkeypatch.setattr(dispatcher, "CONFIG_LOCATIONS", [tmp_path / "absent.json"])
    assert dispatcher.find_config() is None


# --------------------------------------------------------------------------- #
# Missing registry: the printed shape is the interface
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("script_name,extra_key", [
    ("query.py", "protocol"),
    ("query_mysql.py", "ssl_disabled"),
    ("query_postgres.py", "sslmode"),
])
def test_missing_registry_explains_and_exits(script_name, extra_key, tmp_path, monkeypatch, capsys):
    module = _load(script_name, "_dbutils_missing_" + script_name.replace(".", "_"))
    monkeypatch.setattr(module, "CONFIG_LOCATIONS", [tmp_path / "absent.json"])
    with pytest.raises(SystemExit) as caught:
        module.load_config()
    assert caught.value.code == 1
    out = capsys.readouterr().out
    assert out.startswith("Config not found. Searched:\n")
    assert f"  - {tmp_path / 'absent.json'}\n" in out
    assert "\nCreate connections.json with format:\n" in out
    sample = json.loads(out.split("Create connections.json with format:\n", 1)[1])
    entry = sample["databases"][0]
    assert set(entry) == {"name", "description", "host", "port", "database",
                          "user", "password", extra_key}
    assert entry["port"] == (5432 if script_name == "query_postgres.py" else 3306)


def test_explicit_registry_is_read(dispatcher, registry):
    assert dispatcher.load_config(registry) == {"databases": [ENTRY]}


# --------------------------------------------------------------------------- #
# Credential-file permissions
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits")
def test_world_readable_registry_warns(dispatcher, registry, capsys):
    registry.chmod(0o644)
    dispatcher.validate_config_permissions(registry)
    out = capsys.readouterr().out
    assert out == (
        f"WARNING: {registry} has insecure permissions!\n"
        f"Config contains credentials. Run: chmod 600 {registry}\n"
    )


@pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits")
@pytest.mark.parametrize("mode", [0o600, 0o400, 0o700])
def test_owner_only_registry_is_silent(dispatcher, registry, mode, capsys):
    registry.chmod(mode)
    dispatcher.validate_config_permissions(registry)
    assert capsys.readouterr().out == ""


@pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits")
def test_warning_does_not_stop_the_load(dispatcher, registry, capsys):
    registry.chmod(0o604)
    assert dispatcher.load_config(registry) == {"databases": [ENTRY]}
    assert "WARNING" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Entry validation
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_complete_entry_passes(request, handler_name):
    handler = request.getfixturevalue(handler_name)
    assert handler.validate_db_config(dict(ENTRY)) is None


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_missing_fields_are_named_in_order(request, handler_name, capsys):
    handler = request.getfixturevalue(handler_name)
    partial = {"name": "shop", "host": "h"}
    with pytest.raises(SystemExit) as caught:
        handler.validate_db_config(partial)
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == (
        "Error: Database config missing fields: database, user, password"
    )


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_empty_entry_names_every_required_field(request, handler_name, capsys):
    handler = request.getfixturevalue(handler_name)
    with pytest.raises(SystemExit):
        handler.validate_db_config({})
    assert capsys.readouterr().out.strip() == (
        "Error: Database config missing fields: name, host, database, user, password"
    )


# --------------------------------------------------------------------------- #
# Name resolution
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
@pytest.mark.parametrize("spelling", ["shop", "SHOP", "ShOp"])
def test_lookup_ignores_case(request, handler_name, spelling):
    handler = request.getfixturevalue(handler_name)
    config = {"databases": [dict(ENTRY)]}
    assert handler.find_database(config, spelling)["name"] == "shop"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_lookup_miss_lists_the_alternatives(request, handler_name, capsys):
    handler = request.getfixturevalue(handler_name)
    config = {"databases": [dict(ENTRY), dict(ENTRY, name="metrics")]}
    with pytest.raises(SystemExit) as caught:
        handler.find_database(config, "nope")
    assert caught.value.code == 1
    assert capsys.readouterr().out == "Database 'nope' not found.\nAvailable: shop, metrics\n"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_lookup_validates_the_entry_it_returns(request, handler_name, capsys):
    handler = request.getfixturevalue(handler_name)
    with pytest.raises(SystemExit) as caught:
        handler.find_database({"databases": [{"name": "shop"}]}, "shop")
    assert caught.value.code == 1
    assert "missing fields" in capsys.readouterr().out


def test_unnamed_entry_is_reported_as_unnamed(mysql, capsys):
    with pytest.raises(SystemExit):
        mysql.find_database({"databases": [{"host": "h"}]}, "shop")
    assert "Available: unnamed" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Protocol resolution
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("declared,expected", [
    ("mysql", "mysql"),
    ("MYSQL", "mysql"),
    ("postgres", "postgres"),
    ("PostgreSQL", "postgres"),
    ("postgresql", "postgres"),
])
def test_declared_protocol_wins_over_port(dispatcher, declared, expected):
    assert dispatcher.determine_protocol({"protocol": declared, "port": 5432}) == expected


@pytest.mark.parametrize("port,expected", [
    (3306, "mysql"),
    (9030, "mysql"),
    (5432, "postgres"),
    (9005, "postgres"),
])
def test_port_infers_protocol(dispatcher, port, expected):
    assert dispatcher.determine_protocol({"port": port}) == expected


@pytest.mark.parametrize("entry", [{}, {"port": 1234}, {"port": None}, {"port": 0}])
def test_unrecognised_port_falls_back_to_mysql(dispatcher, entry):
    assert dispatcher.determine_protocol(entry) == "mysql"


def test_unknown_protocol_is_refused(dispatcher, capsys):
    with pytest.raises(SystemExit) as caught:
        dispatcher.determine_protocol({"protocol": "Oracle"})
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == (
        "Error: Unknown protocol 'oracle'. Supported: mysql, postgres"
    )


def test_port_map_is_the_published_table(dispatcher):
    assert dispatcher.PORT_PROTOCOL_MAP == {3306: "mysql", 9030: "mysql",
                                           5432: "postgres", 9005: "postgres"}


# --------------------------------------------------------------------------- #
# Handler loading
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("protocol,leaf", [("mysql", "query_mysql.py"),
                                           ("postgres", "query_postgres.py")])
def test_handler_exposes_the_dispatcher_contract(dispatcher, protocol, leaf):
    handler = dispatcher.load_handler(protocol)
    assert Path(handler.__file__).name == leaf
    assert callable(handler.validate_db_config)
    assert callable(handler.execute_query)


def test_unknown_protocol_has_no_handler(dispatcher, capsys):
    with pytest.raises(SystemExit) as caught:
        dispatcher.load_handler("sqlite")
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == "Error: No handler for protocol 'sqlite'"


def test_absent_handler_file_is_named(dispatcher, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(dispatcher, "SCRIPT_DIR", tmp_path)
    with pytest.raises(SystemExit) as caught:
        dispatcher.load_handler("mysql")
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == f"Error: Handler not found: {tmp_path / 'query_mysql.py'}"


# --------------------------------------------------------------------------- #
# --list output shape
# --------------------------------------------------------------------------- #
def test_dispatcher_list_prints_protocol_and_defaults(dispatcher, capsys):
    config = {"databases": [
        dict(ENTRY, protocol="postgres", port=5432),
        {"name": "bare"},
    ]}
    dispatcher.list_databases(config)
    assert capsys.readouterr().out == (
        "Configured databases:\n\n"
        "  [shop]\n"
        "    Protocol: postgres\n"
        "    Host: db.internal:5432\n"
        "    Database: shop\n"
        "    Description: orders, customers\n\n"
        "  [bare]\n"
        "    Protocol: mysql\n"
        "    Host: ?:3306\n"
        "    Database: ?\n"
        "    Description: No description\n\n"
    )


@pytest.mark.parametrize("handler_name,default_port", [("mysql", 3306), ("postgres", 5432)])
def test_handler_list_omits_protocol(request, handler_name, default_port, capsys):
    handler = request.getfixturevalue(handler_name)
    entry = dict(ENTRY)
    entry.pop("port")
    handler.list_databases({"databases": [entry]})
    assert capsys.readouterr().out == (
        "Configured databases:\n\n"
        "  [shop]\n"
        f"    Host: db.internal:{default_port}\n"
        "    Database: shop\n"
        "    Description: orders, customers\n\n"
    )


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_handler_list_validates_each_entry(request, handler_name):
    handler = request.getfixturevalue(handler_name)
    with pytest.raises(SystemExit) as caught:
        handler.list_databases({"databases": [{"name": "shop"}]})
    assert caught.value.code == 1


def test_empty_registry_lists_nothing(dispatcher, capsys):
    dispatcher.list_databases({"databases": []})
    assert capsys.readouterr().out == "Configured databases:\n\n"


# --------------------------------------------------------------------------- #
# Command line: mode precedence and the argument-error paths
# --------------------------------------------------------------------------- #
class _RecordingHandler:
    """Stands in for a protocol handler and records what the dispatcher asked."""

    def __init__(self):
        self.validated = []
        self.calls = []

    def validate_db_config(self, db):
        self.validated.append(db)

    def execute_query(self, db, query, limit=None):
        self.calls.append((query, limit))


@pytest.fixture
def routed(dispatcher, monkeypatch, registry):
    handler = _RecordingHandler()
    monkeypatch.setattr(dispatcher, "load_config", lambda path=None: {"databases": [dict(ENTRY)]})
    monkeypatch.setattr(dispatcher, "load_handler", lambda protocol: handler)
    return handler


def _run_main(module, monkeypatch, argv):
    monkeypatch.setattr(sys, "argv", ["query.py", *argv])
    module.main()


def test_tables_mode_routes_the_mysql_catalog_query(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch, ["--db", "shop", "--tables", "--limit", "7"])
    assert len(routed.calls) == 1
    query, limit = routed.calls[0]
    assert limit == 7
    assert "information_schema.tables" in query
    assert "table_schema = DATABASE()" in query
    for column in ("table_name", "table_type", "engine", "table_rows"):
        assert column in query
    assert routed.validated == [ENTRY]


def test_schema_mode_routes_the_mysql_column_query(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch, ["--db", "shop", "--schema"])
    query, _ = routed.calls[0]
    assert "information_schema.columns" in query
    for column in ("column_name", "data_type", "column_type", "is_nullable",
                   "column_key", "extra"):
        assert column in query
    assert "ordinal_position" in query


def test_query_mode_passes_the_statement_through(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch, ["--db", "shop", "--query", "SELECT 42", "-l", "3"])
    assert routed.calls == [("SELECT 42", 3)]


def test_tables_wins_over_schema_and_query(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch,
              ["--db", "shop", "--query", "SELECT 1", "--schema", "--tables"])
    assert "information_schema.tables" in routed.calls[0][0]


def test_schema_wins_over_query(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch, ["--db", "shop", "--query", "SELECT 1", "--schema"])
    assert "information_schema.columns" in routed.calls[0][0]


def test_list_wins_over_every_mode(dispatcher, routed, monkeypatch, capsys):
    _run_main(dispatcher, monkeypatch, ["--list", "--db", "shop", "--query", "SELECT 1"])
    assert routed.calls == []
    assert "Configured databases:" in capsys.readouterr().out


def test_postgres_entry_routes_the_postgres_catalog_query(dispatcher, monkeypatch):
    handler = _RecordingHandler()
    entry = dict(ENTRY, protocol="postgres", port=5432)
    monkeypatch.setattr(dispatcher, "load_config", lambda path=None: {"databases": [entry]})
    monkeypatch.setattr(dispatcher, "load_handler", lambda protocol: handler)
    _run_main(dispatcher, monkeypatch, ["--db", "shop", "--tables"])
    query, _ = handler.calls[0]
    assert "pg_catalog" in query and "information_schema" in query
    assert "table_schema" in query


def test_missing_db_is_refused(dispatcher, routed, monkeypatch, capsys):
    with pytest.raises(SystemExit) as caught:
        _run_main(dispatcher, monkeypatch, [])
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == (
        "Error: --db required. Use --list to see available databases."
    )


def test_missing_mode_is_refused(dispatcher, routed, monkeypatch, capsys):
    with pytest.raises(SystemExit) as caught:
        _run_main(dispatcher, monkeypatch, ["--db", "shop"])
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == "Error: --query, --tables, or --schema required"


def test_unknown_db_is_refused(dispatcher, routed, monkeypatch, capsys):
    with pytest.raises(SystemExit) as caught:
        _run_main(dispatcher, monkeypatch, ["--db", "ghost", "--query", "SELECT 1"])
    assert caught.value.code == 1
    assert capsys.readouterr().out == "Database 'ghost' not found.\nAvailable: shop\n"


def test_short_options_are_accepted(dispatcher, routed, monkeypatch):
    _run_main(dispatcher, monkeypatch, ["-d", "shop", "-q", "SELECT 1", "-l", "2"])
    assert routed.calls == [("SELECT 1", 2)]


def test_config_option_is_forwarded(dispatcher, monkeypatch, registry):
    seen = []
    monkeypatch.setattr(dispatcher, "load_config",
                        lambda path=None: seen.append(path) or {"databases": []})
    _run_main(dispatcher, monkeypatch, ["--config", str(registry), "--list"])
    assert seen == [registry]


# --------------------------------------------------------------------------- #
# The shipped example registry still parses and still routes
# --------------------------------------------------------------------------- #
def test_example_registry_shape(dispatcher):
    example = json.loads((SKILL / "connections.example.json").read_text(encoding="utf-8"))
    names = [entry["name"] for entry in example["databases"]]
    assert names == ["mysql-prod", "postgres-analytics", "clickhouse-warehouse", "doris-olap"]
    resolved = [dispatcher.determine_protocol(entry) for entry in example["databases"]]
    assert resolved == ["mysql", "postgres", "postgres", "mysql"]
    for entry in example["databases"]:
        assert {"name", "description", "protocol", "host", "port",
                "database", "user", "password"} <= set(entry)


def test_example_registry_entries_are_complete(mysql, postgres):
    example = json.loads((SKILL / "connections.example.json").read_text(encoding="utf-8"))
    for entry in example["databases"]:
        handler = mysql if entry["protocol"] == "mysql" else postgres
        assert handler.validate_db_config(entry) is None


def test_credential_file_is_git_ignored():
    """The registry the setup step creates must never become a tracked file."""
    ignore = (SKILL / ".gitignore").read_text(encoding="utf-8")
    assert "connections.json" in ignore.splitlines()


def test_skill_declares_mit_and_the_framework_classification():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    front = text.split("---\n", 2)[1]
    assert "name: database-utils" in front
    assert "license: MIT" in front
    assert "classification: external" in front
    assert 'skill_id: "<SKILL:.specify/skills/database-utils/SKILL.md>"' in front
    assert "author: ai-engine project" in front
    assert 'version: "3.0"' in front
    assert "Apache-2.0" not in text
    assert "sanjay3290" not in text


def test_license_file_is_mit_with_the_project_copyright():
    text = (SKILL / "LICENSE.txt").read_text(encoding="utf-8")
    assert text.startswith("MIT License")
    assert "Copyright (c) 2026 Qiming Liu and ai-engine contributors" in text
    assert "Apache" not in text


def test_requirements_name_the_two_permissive_drivers():
    lines = [line.strip() for line in
             (SKILL / "requirements.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines == ["PyMySQL", "pg8000"]


def test_anchors_consumed_by_the_declaration_layer_resolve():
    """`no-harness-asset.yaml` names #Overview and the dispatcher as this unit's carrier."""
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "\n## Overview\n" in text
    assert "\n## Usage\n" in text
    assert "scripts/query.py" in text
    declaration = (REPO_ROOT / "shared" / "declarations" / "exclusions"
                   / "no-harness-asset.yaml").read_text(encoding="utf-8")
    assert "anchor: skills/external/database-utils/SKILL.md#Overview" in declaration
    assert "carrier: skills/external/database-utils/scripts/query.py" in declaration
