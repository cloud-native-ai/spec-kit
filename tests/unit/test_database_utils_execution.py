"""Execution, rendering and error paths for database-utils (MIT rewrite).

Every case runs against a recording fake driver: no socket, no server, no real
PyMySQL or pg8000 connection is opened. What is pinned is the observable contract
— the statements sent to put a session into read-only mode, the row cap, the
exact table layout, the truncation marker, credential redaction, and the fact that
a connection is closed on every path including the failing one.

The driver substitution (mysql-connector-python -> PyMySQL, psycopg2 -> pg8000)
is the one place where the rewrite intentionally changes internals; these cases
assert the new drivers are driven correctly while the caller-facing surface stays.
"""

import importlib.util
import ssl
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "skills" / "external" / "database-utils" / "scripts"

ENTRY = {
    "name": "shop",
    "description": "orders",
    "host": "db.internal",
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
def mysql():
    return _load("query_mysql.py", "_dbutils_mysql_exec")


@pytest.fixture(scope="module")
def postgres():
    return _load("query_postgres.py", "_dbutils_postgres_exec")


# --------------------------------------------------------------------------- #
# The fake driver
# --------------------------------------------------------------------------- #
class FakeError(Exception):
    """Stands in for the driver's DB-API error base class."""


class FakeCursor:
    def __init__(self, connection):
        self.connection = connection
        self.executed = []
        self.fetch_sizes = []
        self.closed = False
        self.description = connection.description
        self._rows = list(connection.rows)

    def execute(self, statement, *args):
        self.executed.append(statement)
        for needle, exc in self.connection.fail_on:
            if needle in statement:
                raise exc

    def fetchmany(self, size):
        self.fetch_sizes.append(size)
        taken = self._rows[:size]
        self._rows = self._rows[size:]
        return taken

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, driver, kwargs, rows=(), description=None, fail_on=()):
        self.driver = driver
        self.kwargs = kwargs
        self.rows = rows
        self.description = description
        self.fail_on = list(fail_on)
        self.cursors = []
        self.closed = False
        self.autocommit = None

    def cursor(self):
        cursor = FakeCursor(self)
        self.cursors.append(cursor)
        return cursor

    def close(self):
        self.closed = True

    @property
    def statements(self):
        return [s for cursor in self.cursors for s in cursor.executed]


class FakeDriver:
    """Records connect attempts and hands back pre-programmed connections."""

    Error = FakeError

    def __init__(self, rows=(), description=None, fail_on=(), connect_errors=()):
        self.rows = rows
        self.description = description
        self.fail_on = fail_on
        self.connect_errors = list(connect_errors)
        self.attempts = []
        self.connections = []

    def connect(self, **kwargs):
        self.attempts.append(kwargs)
        if self.connect_errors:
            raise self.connect_errors.pop(0)
        conn = FakeConnection(self, kwargs, self.rows, self.description, self.fail_on)
        self.connections.append(conn)
        return conn


@pytest.fixture
def wired_mysql(mysql, monkeypatch):
    def _wire(**kwargs):
        driver = FakeDriver(**kwargs)
        monkeypatch.setattr(mysql, "_load_driver", lambda: driver)
        return driver
    return _wire


@pytest.fixture
def wired_postgres(postgres, monkeypatch):
    def _wire(**kwargs):
        driver = FakeDriver(**kwargs)
        monkeypatch.setattr(postgres, "_load_driver", lambda: driver)
        return driver
    return _wire


def _entry(**overrides):
    return dict(ENTRY, **overrides)


# --------------------------------------------------------------------------- #
# Connection arguments (the DSN surface)
# --------------------------------------------------------------------------- #
def test_mysql_kwargs_defaults(mysql):
    kwargs = mysql.build_connection_kwargs(_entry())
    assert kwargs == {
        "host": "db.internal", "port": 3306, "database": "shop",
        "user": "reader", "password": "secret", "charset": "utf8mb4",
        "connect_timeout": 10, "autocommit": True,
    }


def test_mysql_kwargs_honour_port_and_ssl_files(mysql):
    kwargs = mysql.build_connection_kwargs(_entry(
        port=9030, ssl_ca="/ca.pem", ssl_cert="/c.pem", ssl_key="/k.pem"))
    assert kwargs["port"] == 9030
    assert kwargs["ssl_ca"] == "/ca.pem"
    assert kwargs["ssl_cert"] == "/c.pem"
    assert kwargs["ssl_key"] == "/k.pem"
    assert "ssl_disabled" not in kwargs


def test_mysql_ssl_disabled_suppresses_the_certificate_files(mysql):
    kwargs = mysql.build_connection_kwargs(_entry(ssl_disabled=True, ssl_ca="/ca.pem"))
    assert kwargs["ssl_disabled"] is True
    assert "ssl_ca" not in kwargs


def test_mysql_partial_ssl_files_are_passed_individually(mysql):
    kwargs = mysql.build_connection_kwargs(_entry(ssl_ca="/ca.pem"))
    assert kwargs["ssl_ca"] == "/ca.pem"
    assert "ssl_cert" not in kwargs and "ssl_key" not in kwargs


def test_postgres_kwargs_defaults(postgres):
    assert postgres.build_connection_kwargs(_entry()) == {
        "host": "db.internal", "port": 5432, "database": "shop",
        "user": "reader", "password": "secret", "timeout": 10,
    }


def test_postgres_kwargs_honour_port(postgres):
    assert postgres.build_connection_kwargs(_entry(port=9005))["port"] == 9005


# --------------------------------------------------------------------------- #
# sslmode policy
# --------------------------------------------------------------------------- #
def test_sslmode_disable_means_no_context(postgres):
    context, opportunistic = postgres._ssl_policy("disable")
    assert context is None and opportunistic is False


@pytest.mark.parametrize("mode", ["allow", "prefer", "require"])
def test_unverified_modes_encrypt_without_authenticating(postgres, mode):
    context, opportunistic = postgres._ssl_policy(mode)
    assert isinstance(context, ssl.SSLContext)
    assert context.verify_mode == ssl.CERT_NONE
    assert context.check_hostname is False
    assert opportunistic is (mode in ("allow", "prefer"))


def test_verify_ca_checks_the_chain_but_not_the_host(postgres):
    context, opportunistic = postgres._ssl_policy("verify-ca")
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is False
    assert opportunistic is False


def test_verify_full_checks_chain_and_host(postgres):
    context, opportunistic = postgres._ssl_policy("verify-full")
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True
    assert opportunistic is False


def test_sslmode_is_case_folded(postgres):
    assert postgres._ssl_policy("DISABLE")[0] is None
    assert postgres._ssl_policy("Verify-Full")[0].check_hostname is True


def test_absent_sslmode_defaults_to_prefer(postgres):
    context, opportunistic = postgres._ssl_policy(None)
    assert context is not None and opportunistic is True


def test_unknown_sslmode_is_refused(postgres, capsys):
    with pytest.raises(SystemExit) as caught:
        postgres._ssl_policy("verify-everything")
    assert caught.value.code == 1
    out = capsys.readouterr().out
    assert out.startswith("Error: Unknown sslmode 'verify-everything'. Supported: ")
    for mode in ("disable", "allow", "prefer", "require", "verify-ca", "verify-full"):
        assert mode in out


# --------------------------------------------------------------------------- #
# Connection attempt order
# --------------------------------------------------------------------------- #
def test_prefer_tries_tls_then_plaintext(postgres, wired_postgres):
    driver = wired_postgres(connect_errors=[FakeError("tls refused")])
    postgres.execute_query(_entry(sslmode="prefer"), "SELECT 1")
    assert len(driver.attempts) == 2
    assert "ssl_context" in driver.attempts[0]
    assert "ssl_context" not in driver.attempts[1]


def test_allow_tries_plaintext_then_tls(postgres, wired_postgres):
    driver = wired_postgres(connect_errors=[FakeError("plaintext refused")])
    postgres.execute_query(_entry(sslmode="allow"), "SELECT 1")
    assert len(driver.attempts) == 2
    assert "ssl_context" not in driver.attempts[0]
    assert "ssl_context" in driver.attempts[1]


def test_require_does_not_fall_back(postgres, wired_postgres, capsys):
    driver = wired_postgres(connect_errors=[FakeError("tls refused")])
    with pytest.raises(SystemExit) as caught:
        postgres.execute_query(_entry(sslmode="require"), "SELECT 1")
    assert caught.value.code == 1
    assert len(driver.attempts) == 1
    assert "Database error: tls refused" in capsys.readouterr().out


def test_disable_never_offers_tls(postgres, wired_postgres):
    driver = wired_postgres()
    postgres.execute_query(_entry(sslmode="disable"), "SELECT 1")
    assert len(driver.attempts) == 1
    assert "ssl_context" not in driver.attempts[0]


def test_default_sslmode_is_prefer(postgres, wired_postgres):
    driver = wired_postgres(connect_errors=[FakeError("tls refused")])
    postgres.execute_query(_entry(), "SELECT 1")
    assert len(driver.attempts) == 2


def test_prefer_surfaces_the_error_when_both_attempts_fail(postgres, wired_postgres, capsys):
    """A real credential failure fails on both transports; the last error is reported."""
    driver = wired_postgres(connect_errors=[FakeError("tls refused"),
                                            FakeError("password authentication failed")])
    with pytest.raises(SystemExit) as caught:
        postgres.execute_query(_entry(sslmode="prefer"), "SELECT 1")
    assert caught.value.code == 1
    assert len(driver.attempts) == 2
    assert capsys.readouterr().out == (
        "Database error: Authentication failed. Check credentials in connections.json\n"
    )


# --------------------------------------------------------------------------- #
# The read-only session is mandatory
# --------------------------------------------------------------------------- #
def test_mysql_session_statements_and_order(mysql, wired_mysql):
    driver = wired_mysql(description=[("a",)], rows=[(1,)])
    mysql.execute_query(_entry(), "SELECT 1")
    conn = driver.connections[0]
    assert conn.statements[:2] == [
        "SET SESSION TRANSACTION READ ONLY",
        "SET SESSION max_execution_time = 30000",
    ]
    assert conn.statements[2] == "SELECT 1"
    assert conn.kwargs["autocommit"] is True


def test_mysql_execution_cap_failure_is_tolerated(mysql, wired_mysql, capsys):
    driver = wired_mysql(description=[("a",)], rows=[(1,)],
                         fail_on=[("max_execution_time", FakeError("unknown variable"))])
    mysql.execute_query(_entry(), "SELECT 1")
    assert "(1 rows)" in capsys.readouterr().out
    assert driver.connections[0].closed is True


def test_mysql_read_only_failure_is_not_tolerated(mysql, wired_mysql, capsys):
    driver = wired_mysql(fail_on=[("READ ONLY", FakeError("not supported"))])
    with pytest.raises(SystemExit) as caught:
        mysql.execute_query(_entry(), "SELECT 1")
    assert caught.value.code == 1
    assert "Database error: not supported" in capsys.readouterr().out
    assert driver.connections[0].closed is True


def test_postgres_session_is_read_only_and_autocommit(postgres, wired_postgres):
    driver = wired_postgres(description=[("a",)], rows=[(1,)])
    postgres.execute_query(_entry(), "SELECT 1")
    conn = driver.connections[0]
    assert conn.autocommit is True
    assert conn.statements[:2] == [
        "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY",
        "SET statement_timeout = 30000",
    ]
    assert conn.statements[2] == "SELECT 1"
    assert len(conn.cursors) == 2
    assert conn.cursors[0].closed is True


def test_postgres_statement_timeout_failure_is_tolerated(postgres, wired_postgres, capsys):
    driver = wired_postgres(description=[("a",)], rows=[(1,)],
                            fail_on=[("statement_timeout", FakeError("unrecognized parameter"))])
    postgres.execute_query(_entry(), "SELECT 1")
    assert "(1 rows)" in capsys.readouterr().out


def test_postgres_read_only_failure_is_not_tolerated(postgres, wired_postgres, capsys):
    driver = wired_postgres(fail_on=[("READ ONLY", FakeError("permission denied"))])
    with pytest.raises(SystemExit) as caught:
        postgres.execute_query(_entry(), "SELECT 1")
    assert caught.value.code == 1
    assert "Database error: permission denied" in capsys.readouterr().out
    assert driver.connections[0].closed is True


# --------------------------------------------------------------------------- #
# The row cap reaches the server
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_limit_is_sent_to_the_server(request, handler_name, wired_mysql, wired_postgres):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(1,)])
    handler.execute_query(_entry(), "SELECT * FROM t", 12)
    assert driver.connections[0].statements[-1] == "SELECT * FROM t LIMIT 12"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_existing_limit_is_not_doubled(request, handler_name, wired_mysql, wired_postgres):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(1,)])
    handler.execute_query(_entry(), "SELECT * FROM t LIMIT 3", 12)
    assert driver.connections[0].statements[-1] == "SELECT * FROM t LIMIT 3"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_fetch_is_capped_at_the_published_maximum(request, handler_name,
                                                  wired_mysql, wired_postgres):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(n,) for n in range(handler.MAX_ROWS + 50)])
    handler.execute_query(_entry(), "SELECT a FROM t")
    cursor = driver.connections[0].cursors[-1]
    assert cursor.fetch_sizes == [handler.MAX_ROWS]


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_single_column_table_layout(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(1,), (22,)])
    handler.execute_query(_entry(), "SELECT a FROM t")
    assert capsys.readouterr().out == "a \n--\n1 \n22\n\n(2 rows)\n"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_null_and_widening(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("id",), ("name",)], rows=[(1, "alice"), (2, None)])
    handler.execute_query(_entry(), "SELECT id, name FROM t")
    assert capsys.readouterr().out == (
        "id | name  \n-----------\n1  | alice \n2  | <NULL>\n\n(2 rows)\n"
    )


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_column_width_is_capped(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("x" * 150,)], rows=[("y" * 150,)])
    handler.execute_query(_entry(), "SELECT x FROM t")
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert lines[0] == "x" * 100
    assert lines[1] == "-" * 100
    assert lines[2] == "y" * 97 + "..."
    assert out.endswith("\n(1 rows)\n")


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_truncation_marker(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(n,) for n in range(handler.MAX_ROWS)])
    handler.execute_query(_entry(), "SELECT a FROM t")
    out = capsys.readouterr().out
    assert out.endswith(f"\n({handler.MAX_ROWS} rows) [truncated at {handler.MAX_ROWS}]\n")


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_below_the_cap_is_not_marked_truncated(request, handler_name,
                                               wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(n,) for n in range(handler.MAX_ROWS - 1)])
    handler.execute_query(_entry(), "SELECT a FROM t")
    out = capsys.readouterr().out
    assert "truncated" not in out
    assert out.endswith(f"\n({handler.MAX_ROWS - 1} rows)\n")


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_empty_result_set_still_prints_the_header(request, handler_name,
                                                  wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",), ("b",)], rows=[])
    handler.execute_query(_entry(), "SELECT a, b FROM t")
    assert capsys.readouterr().out == "a | b\n-----\n\n(0 rows)\n"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_no_result_set_message(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(description=None)
    handler.execute_query(_entry(), "SHOW TABLES")
    assert capsys.readouterr().out == "Query executed (no result set returned)\n"


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_values_are_rendered_with_str(request, handler_name, wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("v",)], rows=[(3.5,), (True,), (b"raw",)])
    handler.execute_query(_entry(), "SELECT v FROM t")
    out = capsys.readouterr().out
    assert "3.5" in out and "True" in out and "b'raw'" in out


# --------------------------------------------------------------------------- #
# Error paths
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("handler_name,server_text", [
    ("mysql", "1045 (28000): Access denied for user 'reader'@'h' (using password: YES)"),
    ("postgres", "password authentication failed for user \"reader\""),
])
def test_credentials_are_redacted(request, handler_name, server_text,
                                  wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        connect_errors=[FakeError(server_text)])
    with pytest.raises(SystemExit) as caught:
        handler.execute_query(_entry(sslmode="disable"), "SELECT 1")
    assert caught.value.code == 1
    assert capsys.readouterr().out == (
        "Database error: Authentication failed. Check credentials in connections.json\n"
    )
    assert driver.attempts


@pytest.mark.parametrize("handler_name,needle", [
    ("mysql", "access denied"),
    ("postgres", "authentication"),
])
def test_redaction_triggers_on_the_family_keyword(request, handler_name, needle,
                                                  wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        connect_errors=[FakeError("server said: " + needle.upper())])
    with pytest.raises(SystemExit):
        handler.execute_query(_entry(sslmode="disable"), "SELECT 1")
    assert "Authentication failed." in capsys.readouterr().out


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_ordinary_server_error_is_reported_verbatim(request, handler_name,
                                                    wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        connect_errors=[FakeError("1146 (42S02): Table 'shop.t' doesn't exist")])
    with pytest.raises(SystemExit) as caught:
        handler.execute_query(_entry(sslmode="disable"), "SELECT * FROM t")
    assert caught.value.code == 1
    assert capsys.readouterr().out == (
        "Database error: 1146 (42S02): Table 'shop.t' doesn't exist\n"
    )


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_statement_failure_closes_cursor_and_connection(request, handler_name,
                                                        wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        fail_on=[("SELECT boom", FakeError("syntax error"))])
    with pytest.raises(SystemExit) as caught:
        handler.execute_query(_entry(), "SELECT boom")
    assert caught.value.code == 1
    conn = driver.connections[0]
    assert conn.closed is True
    assert all(cursor.closed for cursor in conn.cursors)
    assert "Database error: syntax error" in capsys.readouterr().out


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_success_closes_cursor_and_connection(request, handler_name,
                                              wired_mysql, wired_postgres):
    handler = request.getfixturevalue(handler_name)
    driver = (wired_mysql if handler_name == "mysql" else wired_postgres)(
        description=[("a",)], rows=[(1,)])
    handler.execute_query(_entry(), "SELECT 1")
    conn = driver.connections[0]
    assert conn.closed is True
    assert all(cursor.closed for cursor in conn.cursors)


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_oserror_is_reported_as_a_database_error(request, handler_name,
                                                 wired_mysql, wired_postgres, capsys):
    handler = request.getfixturevalue(handler_name)
    (wired_mysql if handler_name == "mysql" else wired_postgres)(
        connect_errors=[OSError("name resolution failed")])
    with pytest.raises(SystemExit) as caught:
        handler.execute_query(_entry(sslmode="disable"), "SELECT 1")
    assert caught.value.code == 1
    assert capsys.readouterr().out == "Database error: name resolution failed\n"


# --------------------------------------------------------------------------- #
# A missing driver is reported at connect time, not at import time
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("script_name,module_name,distribution", [
    ("query_mysql.py", "pymysql", "PyMySQL"),
    ("query_postgres.py", "pg8000", "pg8000"),
])
def test_missing_driver_prints_the_install_hint(script_name, module_name, distribution,
                                                monkeypatch, capsys):
    handler = _load(script_name, "_dbutils_nodriver_" + module_name)
    monkeypatch.setitem(sys.modules, module_name, None)
    with pytest.raises(SystemExit) as caught:
        handler._load_driver()
    assert caught.value.code == 1
    assert capsys.readouterr().out == (
        f"Error: {distribution} not installed. Run: pip install {distribution}\n"
    )


@pytest.mark.parametrize("script_name", ["query_mysql.py", "query_postgres.py"])
def test_module_loads_without_any_driver(script_name, monkeypatch):
    """The flag surface and --list must not depend on a driver being installed."""
    monkeypatch.setitem(sys.modules, "pymysql", None)
    monkeypatch.setitem(sys.modules, "pg8000", None)
    handler = _load(script_name, "_dbutils_driverless_" + script_name.replace(".", "_"))
    assert callable(handler.main)
    assert handler.is_read_only("SELECT 1") is True


@pytest.mark.parametrize("handler_name", ["mysql", "postgres"])
def test_missing_driver_exits_one_from_execute_query(request, handler_name, monkeypatch, capsys):
    handler = request.getfixturevalue(handler_name)
    module_name = "pymysql" if handler_name == "mysql" else "pg8000"
    monkeypatch.setitem(sys.modules, module_name, None)
    with pytest.raises(SystemExit) as caught:
        handler.execute_query(_entry(), "SELECT 1")
    assert caught.value.code == 1
    assert "not installed. Run: pip install" in capsys.readouterr().out
