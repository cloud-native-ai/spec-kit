#!/usr/bin/env python3
"""Read-only query runner for the MySQL wire protocol.

Speaks to MySQL and MariaDB directly, and to the MySQL-compatible front ends of
Apache Doris and SelectDB.  Two independent layers keep a run from writing: the
statement is screened here before it is sent, and the server session is switched
to read-only access mode so anything that slips past the screen is still refused.

Driver: PyMySQL (MIT).  ai-engine project, MIT licensed -- see LICENSE.txt.
"""

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Optional

# The skill root, i.e. the directory that holds SKILL.md and connections.json.
SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_LOCATIONS = [
    SCRIPT_DIR / "connections.json",
    Path.home() / ".config" / "claude" / "mysql-connections.json",
]

MAX_ROWS = 10000
MAX_COLUMN_WIDTH = 100
QUERY_TIMEOUT_MS = 30000
CONNECTION_TIMEOUT_SEC = 10
NULL_DISPLAY = "<NULL>"

DEFAULT_PORT = 3306
REQUIRED_FIELDS = ("name", "host", "database", "user", "password")
SSL_FILE_FIELDS = ("ssl_ca", "ssl_cert", "ssl_key")

# A statement is accepted on its leading keyword alone, after case folding and
# trimming -- the same screen the server-side read-only mode backs up.
_LEADING_KEYWORD = re.compile(r"^(SELECT|SHOW|DESCRIBE|EXPLAIN|WITH|DESC)")
# SELECT ... INTO OUTFILE writes a server-side file and is not covered by the
# read-only access mode, so it is refused outright.
_SERVER_FILE_WRITE = re.compile(r"\bINTO\s+(OUTFILE|DUMPFILE)\b", re.IGNORECASE)
_EXISTING_LIMIT = re.compile(r"\bLIMIT\s+\d+", re.IGNORECASE)

_REFUSAL = "Error: Only read-only queries (SELECT, SHOW, DESCRIBE, EXPLAIN) are allowed."
_MULTI_STATEMENT = "Error: Multiple statements not allowed. Execute queries separately."
_AUTH_HINT = "Authentication failed. Check credentials in connections.json"

_TABLES_SQL = (
    "SELECT table_name, table_type, engine, table_rows "
    "FROM information_schema.tables "
    "WHERE table_schema = DATABASE() "
    "ORDER BY table_name"
)
_SCHEMA_SQL = (
    "SELECT c.table_name, c.column_name, c.data_type, c.column_type, "
    "c.is_nullable, c.column_key, c.extra "
    "FROM information_schema.columns c "
    "JOIN information_schema.tables t "
    "ON c.table_name = t.table_name AND c.table_schema = t.table_schema "
    "WHERE c.table_schema = DATABASE() "
    "ORDER BY c.table_name, c.ordinal_position"
)


def is_read_only(query: str) -> bool:
    """Screen a statement client side; the read-only session is the real barrier."""
    folded = query.upper().strip()
    if not _LEADING_KEYWORD.match(folded):
        return False
    return _SERVER_FILE_WRITE.search(folded) is None


def validate_single_statement(query: str) -> bool:
    """True when nothing but a trailing terminator separates one statement."""
    trimmed = query.rstrip().rstrip(";")
    return ";" not in trimmed


def validate_config_permissions(path: Path) -> None:
    """Warn about a credential file that group or other can reach (POSIX only)."""
    if os.name == "nt":
        return
    mode = path.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        print(f"WARNING: {path} has insecure permissions!")
        print(f"Config contains credentials. Run: chmod 600 {path}")


def validate_db_config(db: dict) -> None:
    """Exit unless every field a connection needs is present."""
    absent = [field for field in REQUIRED_FIELDS if field not in db]
    if absent:
        print(f"Error: Database config missing fields: {', '.join(absent)}")
        sys.exit(1)


def find_config() -> Optional[Path]:
    """First existing candidate, or None."""
    for candidate in CONFIG_LOCATIONS:
        if candidate.exists():
            return candidate
    return None


def _config_template() -> dict:
    """The entry shape printed when no config could be located."""
    return {
        "databases": [{
            "name": "mydb",
            "description": "Description of database contents",
            "host": "localhost",
            "port": DEFAULT_PORT,
            "database": "mydb",
            "user": "user",
            "password": "password",
            "ssl_disabled": False,
        }]
    }


def load_config(config_path: Optional[Path] = None) -> dict:
    """Read the connection registry, or explain how to create one and exit 1."""
    path = config_path or find_config()
    if path is None:
        print("Config not found. Searched:")
        for candidate in CONFIG_LOCATIONS:
            print(f"  - {candidate}")
        print("\nCreate connections.json with format:")
        print(json.dumps(_config_template(), indent=2))
        sys.exit(1)

    validate_config_permissions(path)
    with open(path) as handle:
        return json.load(handle)


def list_databases(config: dict) -> None:
    """Print one block per configured entry."""
    print("Configured databases:\n")
    for db in config.get("databases", []):
        validate_db_config(db)
        print(f"  [{db['name']}]")
        print(f"    Host: {db['host']}:{db.get('port', DEFAULT_PORT)}")
        print(f"    Database: {db['database']}")
        print(f"    Description: {db.get('description', 'No description')}")
        print()


def build_connection_kwargs(db_config: dict) -> dict:
    """Translate a config entry into PyMySQL connection arguments."""
    kwargs = {
        "host": db_config["host"],
        "port": db_config.get("port", DEFAULT_PORT),
        "database": db_config["database"],
        "user": db_config["user"],
        "password": db_config["password"],
        "charset": "utf8mb4",
        "connect_timeout": CONNECTION_TIMEOUT_SEC,
        "autocommit": True,
    }
    if db_config.get("ssl_disabled"):
        kwargs["ssl_disabled"] = True
        return kwargs
    for field in SSL_FILE_FIELDS:
        if db_config.get(field):
            kwargs[field] = db_config[field]
    return kwargs


def _load_driver():
    """Import PyMySQL on demand so the flag surface answers without it."""
    try:
        import pymysql
    except ImportError:
        print("Error: PyMySQL not installed. Run: pip install PyMySQL")
        sys.exit(1)
    return pymysql


def _redact(message: str) -> str:
    """Keep credential material out of the printed error."""
    lowered = message.lower()
    if "password" in lowered or "access denied" in lowered:
        return _AUTH_HINT
    return message


def _apply_limit(query: str, limit: Optional[int]) -> str:
    """Append a row cap only when the statement does not already carry one."""
    if limit and not _EXISTING_LIMIT.search(query):
        return query.rstrip(";") + f" LIMIT {limit}"
    return query


def _cell(value) -> str:
    return NULL_DISPLAY if value is None else str(value)


def _print_result(columns, rows) -> None:
    """Render a fixed-width table with a per-column cap and a row-count footer."""
    headings = [str(name)[:MAX_COLUMN_WIDTH] for name in columns]
    body = [[_cell(value) for value in row] for row in rows]

    widths = [len(heading) for heading in headings]
    for cells in body:
        for index, text in enumerate(cells):
            widths[index] = max(widths[index], len(text))
    widths = [min(width, MAX_COLUMN_WIDTH) for width in widths]

    header = " | ".join(
        heading.ljust(widths[index]) for index, heading in enumerate(headings)
    )
    print(header)
    print("-" * len(header))

    for cells in body:
        rendered = []
        for index, text in enumerate(cells):
            if len(text) > MAX_COLUMN_WIDTH:
                text = text[:MAX_COLUMN_WIDTH - 3] + "..."
            rendered.append(text.ljust(widths[index]))
        print(" | ".join(rendered))

    footer = f"\n({len(rows)} rows)"
    if len(rows) == MAX_ROWS:
        footer += f" [truncated at {MAX_ROWS}]"
    print(footer)


def _prepare_session(cursor, driver) -> None:
    """Read-only access mode is mandatory; the execution cap is best effort."""
    cursor.execute("SET SESSION TRANSACTION READ ONLY")
    try:
        cursor.execute(f"SET SESSION max_execution_time = {QUERY_TIMEOUT_MS}")
    except driver.Error:
        # MariaDB and older MySQL builds do not know this variable.
        pass


def execute_query(db_config: dict, query: str, limit: Optional[int] = None) -> None:
    """Screen, run and render one read-only statement; exit 1 on any refusal."""
    if not is_read_only(query):
        print(_REFUSAL)
        sys.exit(1)
    if not validate_single_statement(query):
        print(_MULTI_STATEMENT)
        sys.exit(1)

    statement = _apply_limit(query, limit)
    driver = _load_driver()
    conn = None
    try:
        conn = driver.connect(**build_connection_kwargs(db_config))
        cursor = conn.cursor()
        try:
            _prepare_session(cursor, driver)
            cursor.execute(statement)
            if not cursor.description:
                print("Query executed (no result set returned)")
            else:
                columns = [field[0] for field in cursor.description]
                _print_result(columns, cursor.fetchmany(MAX_ROWS))
        finally:
            cursor.close()
    except (driver.Error, OSError) as exc:
        print(f"Database error: {_redact(str(exc))}")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()


def find_database(config: dict, name: str) -> dict:
    """Resolve an entry by name, ignoring case."""
    wanted = name.lower()
    for db in config.get("databases", []):
        if db.get("name", "").lower() == wanted:
            validate_db_config(db)
            return db
    known = [db.get("name", "unnamed") for db in config.get("databases", [])]
    print(f"Database '{name}' not found.")
    print(f"Available: {', '.join(known)}")
    sys.exit(1)


def main() -> None:
    """Parse the command line and dispatch to the selected read-only mode."""
    parser = argparse.ArgumentParser(
        description="Execute read-only MySQL queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list
  %(prog)s --db mydb --tables
  %(prog)s --db mydb --query "SELECT * FROM users" --limit 100
        """
    )
    parser.add_argument("--config", "-c", type=Path, help="Path to config JSON")
    parser.add_argument("--db", "-d", help="Database name to query")
    parser.add_argument("--query", "-q", help="SQL query to execute")
    parser.add_argument("--limit", "-l", type=int, help="Limit rows returned")
    parser.add_argument("--list", action="store_true", help="List configured databases")
    parser.add_argument("--schema", "-s", action="store_true", help="Show database schema")
    parser.add_argument("--tables", "-t", action="store_true", help="List tables")

    args = parser.parse_args()
    config = load_config(args.config)

    if args.list:
        list_databases(config)
        return

    if not args.db:
        print("Error: --db required. Use --list to see available databases.")
        sys.exit(1)

    db_config = find_database(config, args.db)

    if args.tables:
        execute_query(db_config, _TABLES_SQL, args.limit)
    elif args.schema:
        execute_query(db_config, _SCHEMA_SQL, args.limit)
    elif args.query:
        execute_query(db_config, args.query, args.limit)
    else:
        print("Error: --query, --tables, or --schema required")
        sys.exit(1)


#
# Emitted by `scripts/python/sync-mirrors.py`; the authority for this block is
# `contracts/mirror-projection.contract.md` C-34 / C-36. It depends on nothing
# that exists only in the source tree: it re-derives its own version line (C-36).
_VERSION_SOURCE = "pyproject.toml"
_VERSION_QUOTES = chr(39) + chr(34)
_MAX_UPWARD_LEVELS = 12


def _bridge_version(start):
    _here = start.resolve()
    for _ in range(_MAX_UPWARD_LEVELS + 1):
        if (_here / _VERSION_SOURCE).is_file() and (_here / ".git").exists():
            try:
                _text = (_here / _VERSION_SOURCE).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return "unknown"
            _in_project = False
            for _raw in _text.splitlines():
                _line = _raw.strip()
                if not _line or _line.startswith("#"):
                    continue
                if _line.startswith("[") and _line.endswith("]"):
                    _in_project = _line == "[project]"
                    continue
                if not _in_project:
                    continue
                _key, _sep, _value = _line.partition("=")
                if _sep and _key.strip() == "version":
                    _value = _value.strip()
                    if len(_value) >= 2 and _value[0] == _value[-1] and _value[0] in _VERSION_QUOTES:
                        _value = _value[1:-1]
                    return _value or "unknown"
            return "unknown"
        if _here.parent == _here:
            return "unknown"
        _here = _here.parent
    return "unknown"

def _bridge_main():
    import sys as _bridge_sys
    from pathlib import Path as _bridge_path

    _argv = list(_bridge_sys.argv[1:])
    if "--version" not in _argv:
        return
    if "--" in _argv and _argv.index("--version") > _argv.index("--"):
        return
    _invoked = _bridge_sys.argv[0] if _bridge_sys.argv[0] else "."
    _name = _bridge_path(_invoked).name or "script"
    print("%s %s" % (_name, _bridge_version(_bridge_path(_invoked).resolve().parent)))
    raise SystemExit(0)


_bridge_main()
del _bridge_main
# script-interface:86:begin (feature 086 -- generated; the rule is owned by
# `shared/definitions/script-interface-definitions.md`, its executable form by
# `scripts/python/script_interface_cli.py`. This block owns no rule of its own.)
import sys as _sig_sys
import pathlib as _sig_pathlib

_SIG_OWNER = _sig_pathlib.Path(__file__).resolve().parent
while not ((_SIG_OWNER / 'pyproject.toml').is_file()
           and (_SIG_OWNER / '.git').exists()) and _SIG_OWNER.parent != _SIG_OWNER:
    _SIG_OWNER = _SIG_OWNER.parent
_SIG_OWNER = str(_SIG_OWNER / 'scripts' / 'python')
if _SIG_OWNER not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_OWNER)

_SIG_SCRIPT = 'skills/external/database-utils/scripts/query_mysql.py'
_SIG_DECLARED = ('--config', '--db', '--limit', '--list', '--query', '--schema', '--tables', '-c', '-d', '-l', '-q', '-s', '-t')
_SIG_HELP = (
    'usage: query_mysql.py [options]\n'
    'options:\n'
    '  --config\n  --db\n  --limit\n  --list\n  --query\n  --schema\n  --tables\n  -c\n  -d\n  -l\n  -q\n  -s\n  -t\n'
    '  -h, --help    print this help and exit\n'
    '  --version     print the script name and the framework version, then exit\n'
    +
    'side-effects:' + ' ' + 'writes only through the options it documents; a flag-only invocation writes nothing' + '\n'
    +
    'exit-codes:' + ' ' + '0 success; 1 a documented check failed; 2 argument or environment error' + '\n'
)


def _sig_guard(argv):
    # Answer the flags and reject an undeclared option before any parsing or write.
    # RULES are asked of the owner (script_interface_cli.guard_argv), never restated:
    # the declared vocabulary and the flag forms are its, and C-9 (a recognized option
    # never rescues an unrecognized one) is its judgement. What stays local is the help
    # BODY, because its operand sentence is this script's own.
    try:
        import script_interface_cli as _sig  # noqa: E402 -- deferred: a copied script may lack it
    except ImportError:  # skill-local or sandbox copy: the module's own parser still runs
        return list(argv)
    line = list(argv)
    try:
        _sig.guard_argv(line, declared=_SIG_DECLARED)
    except SystemExit as answered:  # what guard_argv raises; _sig_sys.exit IS SystemExit
        if answered.code == 0:
            raise
        # The owner prints the rejection line and this script's help body is appended after
        # it, so the reader sees the vocabulary and not only the refusal.
        _sig_sys.stderr.write(_SIG_HELP)
        raise _sig_sys.exit(answered.code)
    stop = line.index('--') if '--' in line else len(line)
    if '-h' in line[:stop] or '--help' in line[:stop]:
        _sig_sys.stdout.write(_SIG_HELP)
        raise _sig_sys.exit(0)
    return line

if __name__ == "__main__":
    _sig_sys.argv = [_sig_sys.argv[0]] + _sig_guard(_sig_sys.argv[1:])
# script-interface:86:end

if __name__ == "__main__":
    main()
