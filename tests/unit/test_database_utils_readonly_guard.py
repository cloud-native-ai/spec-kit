"""Read-only screening contract for the database-utils handlers (MIT rewrite).

The skill's safety claim is two-layered: a client-side screen and a server-side
read-only session. This module pins the CLIENT layer's accepted and refused
vocabulary for both protocol handlers, plus the single-statement rule and the row
cap injection. Everything runs in-process against the real script files; no
driver, no server and no socket is involved.

The rewrite replaced an Apache-2.0 implementation with an original MIT one while
keeping the interface. These cases are the decidable form of "the guard semantics
survived": each one names a statement and the verdict it must get.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "database-utils" / "scripts"


def _load(script_name: str, module_name: str):
    """Execute one handler file as a module, restoring the interpreter state.

    The scripts carry a generated interface block that prepends the framework's
    ``scripts/python`` to ``sys.path``; that is a global mutation, so it is undone
    here to keep this module from coupling to any other test's import surface.
    """
    path = SCRIPTS / script_name
    assert path.is_file(), f"handler missing: {path}"
    saved_path = list(sys.path)
    saved_argv = list(sys.argv)
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
def mysql():
    return _load("query_mysql.py", "_dbutils_mysql_guard")


@pytest.fixture(scope="module")
def postgres():
    return _load("query_postgres.py", "_dbutils_postgres_guard")


# --------------------------------------------------------------------------- #
# The accepted lead keywords
# --------------------------------------------------------------------------- #
MYSQL_ACCEPTED = [
    "SELECT 1",
    "select * from users",
    "  SELECT 1  ",
    "SHOW TABLES",
    "SHOW CREATE TABLE users",
    "DESCRIBE users",
    "DESC users",
    "EXPLAIN SELECT 1",
    "WITH x AS (SELECT 1) SELECT * FROM x",
]

POSTGRES_ACCEPTED = [
    "SELECT 1",
    "select * from users",
    "\tSELECT 1\n",
    "SHOW search_path",
    "DESCRIBE users",
    "EXPLAIN SELECT 1",
    "WITH x AS (SELECT 1) SELECT * FROM x",
    "\\d users",
]

MYSQL_REFUSED = [
    "INSERT INTO t VALUES (1)",
    "UPDATE t SET a = 1",
    "DELETE FROM t",
    "DROP TABLE t",
    "TRUNCATE t",
    "CREATE TABLE t (a int)",
    "ALTER TABLE t ADD COLUMN b int",
    "GRANT ALL ON t TO u",
    "CALL some_proc()",
    "SET autocommit = 0",
    "LOAD DATA INFILE '/tmp/x' INTO TABLE t",
    "",
    "   ",
]

POSTGRES_REFUSED = [
    "INSERT INTO t VALUES (1)",
    "UPDATE t SET a = 1",
    "DELETE FROM t",
    "DROP TABLE t",
    "TRUNCATE t",
    "CREATE TABLE t (a int)",
    "VACUUM",
    "COPY t FROM '/tmp/x'",
    "SET statement_timeout = 0",
    "",
    "   ",
]


@pytest.mark.parametrize("statement", MYSQL_ACCEPTED)
def test_mysql_screen_accepts_read_leads(mysql, statement):
    assert mysql.is_read_only(statement) is True


@pytest.mark.parametrize("statement", MYSQL_REFUSED)
def test_mysql_screen_refuses_write_leads(mysql, statement):
    assert mysql.is_read_only(statement) is False


@pytest.mark.parametrize("statement", POSTGRES_ACCEPTED)
def test_postgres_screen_accepts_read_leads(postgres, statement):
    assert postgres.is_read_only(statement) is True


@pytest.mark.parametrize("statement", POSTGRES_REFUSED)
def test_postgres_screen_refuses_write_leads(postgres, statement):
    assert postgres.is_read_only(statement) is False


def test_desc_is_mysql_only(postgres, mysql):
    """The two families differ on `DESC` and on the psql meta-command."""
    assert mysql.is_read_only("DESC users") is True
    assert postgres.is_read_only("DESC users") is False
    assert postgres.is_read_only("\\D users") is True
    assert mysql.is_read_only("\\d users") is False


# --------------------------------------------------------------------------- #
# Server-side file writes are refused even though the lead keyword is a read
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("statement", [
    "SELECT a INTO OUTFILE '/tmp/x' FROM t",
    "select a into outfile '/tmp/x' from t",
    "SELECT a INTO   DUMPFILE '/tmp/x' FROM t",
    "SELECT a INTO\nOUTFILE '/tmp/x' FROM t",
    "WITH x AS (SELECT 1) SELECT a INTO OUTFILE '/tmp/y' FROM x",
])
def test_mysql_screen_refuses_server_file_writes(mysql, statement):
    assert mysql.is_read_only(statement) is False


def test_postgres_screen_has_no_outfile_clause(postgres):
    """The PostgreSQL handler's screen is the lead keyword; COPY is refused by it."""
    assert postgres.is_read_only("COPY t TO '/tmp/x'") is False


def test_screen_is_a_lead_check_not_a_proof(mysql):
    """A read lead can still hide a write — the server session is the second layer.

    Pinning this honestly matters: a test that claimed the screen catches every
    write would be asserting something the implementation does not do.
    """
    assert mysql.is_read_only("WITH x AS (SELECT 1) DELETE FROM t") is True


# --------------------------------------------------------------------------- #
# One statement per invocation
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
@pytest.mark.parametrize("statement,expected", [
    ("SELECT 1", True),
    ("SELECT 1;", True),
    ("SELECT 1;;", True),
    ("SELECT 1;  ", True),
    ("SELECT 1\n", True),
    ("SELECT 1; DROP TABLE t", False),
    ("SELECT 1;SELECT 2", False),
    ("SELECT ';'", False),
    (";", True),
])
def test_single_statement_rule(request, handler_name, statement, expected):
    handler = request.getfixturevalue(handler_name)
    assert handler.validate_single_statement(statement) is expected


def test_trailing_terminator_is_stripped_before_the_semicolon_scan(mysql):
    """Whitespace after the terminator must not turn one statement into two."""
    assert mysql.validate_single_statement("SELECT 1;\n\t  ") is True


# --------------------------------------------------------------------------- #
# Row cap injection
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_limit_is_appended_when_absent(request, handler_name):
    handler = request.getfixturevalue(handler_name)
    assert handler._apply_limit("SELECT * FROM t", 25) == "SELECT * FROM t LIMIT 25"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_limit_is_appended_after_the_terminator_only(request, handler_name):
    handler = request.getfixturevalue(handler_name)
    assert handler._apply_limit("SELECT * FROM t;", 25) == "SELECT * FROM t LIMIT 25"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
@pytest.mark.parametrize("statement", [
    "SELECT * FROM t LIMIT 5",
    "select * from t limit 5",
    "SELECT * FROM t LIMIT  5",
    "SELECT * FROM t LIMIT\n5",
])
def test_existing_limit_wins(request, handler_name, statement):
    handler = request.getfixturevalue(handler_name)
    assert handler._apply_limit(statement, 25) == statement


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
@pytest.mark.parametrize("limit", [None, 0])
def test_absent_or_zero_limit_leaves_the_statement_alone(request, handler_name, limit):
    handler = request.getfixturevalue(handler_name)
    assert handler._apply_limit("SELECT * FROM t", limit) == "SELECT * FROM t"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_limit_inside_a_literal_is_not_treated_as_a_clause(request, handler_name):
    """The cap is matched as a keyword, so a quoted word alone does not suppress it."""
    handler = request.getfixturevalue(handler_name)
    assert handler._apply_limit("SELECT 'limit' FROM t", 5) == "SELECT 'limit' FROM t LIMIT 5"


# --------------------------------------------------------------------------- #
# The refusal messages and exit codes are part of the interface
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name,needle", [
    ("mysql", "Error: Only read-only queries (SELECT, SHOW, DESCRIBE, EXPLAIN) are allowed."),
    ("postgres", "Error: Only read-only queries (SELECT, SHOW, EXPLAIN) are allowed."),
])
def test_write_refusal_message_and_exit(request, handler_name, needle, capsys):
    handler = request.getfixturevalue(handler_name)
    with pytest.raises(SystemExit) as caught:
        handler.execute_query({"name": "d", "host": "h", "database": "db",
                               "user": "u", "password": "p"}, "DELETE FROM t")
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == needle


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_multi_statement_refusal_message_and_exit(request, handler_name, capsys):
    handler = request.getfixturevalue(handler_name)
    with pytest.raises(SystemExit) as caught:
        handler.execute_query({"name": "d", "host": "h", "database": "db",
                               "user": "u", "password": "p"}, "SELECT 1; DROP TABLE t")
    assert caught.value.code == 1
    assert capsys.readouterr().out.strip() == (
        "Error: Multiple statements not allowed. Execute queries separately."
    )


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_refusal_never_opens_a_connection(request, handler_name, monkeypatch):
    """The screen runs before the driver is even loaded."""
    handler = request.getfixturevalue(handler_name)

    def _no_driver():
        raise AssertionError("driver loaded for a refused statement")

    monkeypatch.setattr(handler, "_load_driver", _no_driver)
    with pytest.raises(SystemExit):
        handler.execute_query({"name": "d", "host": "h", "database": "db",
                               "user": "u", "password": "p"}, "DROP TABLE t")


# --------------------------------------------------------------------------- #
# The published constants are the caps the documentation names
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_published_caps(request, handler_name):
    handler = request.getfixturevalue(handler_name)
    assert handler.MAX_ROWS == 10000
    assert handler.MAX_COLUMN_WIDTH == 100
    assert handler.QUERY_TIMEOUT_MS == 30000
    assert handler.CONNECTION_TIMEOUT_SEC == 10
    assert handler.NULL_DISPLAY == "<NULL>"
