# Setting Up and Using database-utils

A practical guide to connecting this skill to a server and reading data from it. The command
vocabulary and the field tables live in `SKILL.md`; this file walks the setup once and then shows
what a working session looks like.

## 1. Install the drivers

The skill is pure Python. Two drivers cover the two wire protocols, and neither needs a compiler
or a system client library:

```bash
pip install -r requirements.txt
```

| Driver | License | Reaches |
|--------|---------|---------|
| `PyMySQL` | MIT | MySQL, MariaDB, Apache Doris, SelectDB |
| `pg8000` | BSD-3-Clause | PostgreSQL, ClickHouse over its PostgreSQL front end |

Install only what you query. `--help`, `--version` and `--list` work with no driver at all; a
missing driver is reported with its install command at the moment a connection is attempted.

## 2. Author the registry

Start from the shipped example and edit it in place:

```bash
cp connections.example.json connections.json
chmod 600 connections.json
```

The file is a single object with a `databases` array. One entry per server:

```json
{
  "databases": [
    {
      "name": "shop-mysql",
      "description": "Storefront MySQL - customers, orders, payments",
      "protocol": "mysql",
      "host": "mysql.internal",
      "port": 3306,
      "database": "shop",
      "user": "report_reader",
      "password": "replace-me",
      "ssl_disabled": false
    },
    {
      "name": "metrics-pg",
      "description": "Metrics PostgreSQL - daily aggregates, dashboards",
      "protocol": "postgres",
      "host": "pg.internal",
      "port": 5432,
      "database": "metrics",
      "user": "report_reader",
      "password": "replace-me",
      "sslmode": "verify-full"
    }
  ]
}
```

Three habits make the registry useful later:

- **Write the description for a reader who has not seen the schema.** It is the field used to pick
  an entry from a topic, so "orders, payments, refunds" beats "prod db".
- **Name the protocol explicitly** unless the server sits on its family's standard port. Inference
  covers 3306 and 9030 for MySQL, 5432 and 9005 for PostgreSQL, and falls back to MySQL otherwise.
- **Use a read-only login.** The skill refuses writes on its own, but a server account that cannot
  write is the layer that holds even if the client is bypassed.

`connections.json` is ignored by git in this skill directory. Keep it that way: the file holds
passwords.

### Where the file is looked up

| Entry point | First location | Second location |
|-------------|----------------|-----------------|
| `.specify/scripts/query.py` | `<skill>/connections.json` | `~/.config/claude/db-connections.json` |
| `.specify/scripts/query_mysql.py` | `<skill>/connections.json` | `~/.config/claude/mysql-connections.json` |
| `.specify/scripts/query_postgres.py` | `<skill>/connections.json` | `~/.config/claude/postgres-connections.json` |

The first existing file wins. `--config <path>` overrides the search entirely, which is how a
temporary or per-project registry is used without touching the skill directory.

A registry that group or other can read produces a warning naming `chmod 600`; the run continues.

## 3. TLS per family

**MySQL family.** TLS is on by default. Point `ssl_ca` at the issuing CA, and add `ssl_cert` /
`ssl_key` when the server requires a client certificate. For a local server with no TLS at all,
set `"ssl_disabled": true`.

**PostgreSQL family.** `sslmode` takes the libpq vocabulary:

| Value | Encrypts | Validates chain | Validates host |
|-------|----------|-----------------|----------------|
| `disable` | no | — | — |
| `allow` | when the server offers it | no | no |
| `prefer` (default) | when the server offers it | no | no |
| `require` | yes | no | no |
| `verify-ca` | yes | yes | no |
| `verify-full` | yes | yes | yes |

`allow` tries plaintext first and `prefer` tries TLS first; both fall back to the other transport
when the first attempt fails. Choose `verify-full` whenever the server certificate can be
validated, and `verify-ca` with a scoped CA bundle when the host name does not match the
certificate. The unverified modes are a deliberate per-entry tradeoff for private-CA hosts, not a
recommendation.

## 4. A working session

```bash
# 1. What can I reach?
python3 .specify/scripts/query.py --list

# 2. What is in it?
python3 .specify/scripts/query.py --db shop-mysql --tables

# 3. What do the columns look like?
python3 .specify/scripts/query.py --db shop-mysql --schema

# 4. Ask the question, with a cap.
python3 .specify/scripts/query.py --db shop-mysql \
  --query "SELECT status, COUNT(*) AS n FROM orders GROUP BY status" --limit 50

# 5. The same question on the other family.
python3 .specify/scripts/query.py --db metrics-pg \
  --query "SELECT day, signups FROM daily ORDER BY day DESC" --limit 30
```

A result prints as a header row, a dash rule, one line per row, then `(N rows)`. `NULL` shows as
`<NULL>`, a column never exceeds 100 characters, and a fetch that hits the 10,000-row ceiling says
`[truncated at 10000]` in the footer. When you see that marker, narrow the statement rather than
reporting the partial answer as complete.

`--limit` is appended only when the statement has no `LIMIT <number>` of its own, so an explicit
`LIMIT` in the SQL always wins.

### Reaching a handler directly

The dispatcher is the normal path. The handlers are callable on their own when the protocol is
already known, which skips routing:

```bash
python3 .specify/scripts/query_mysql.py --db shop-mysql --tables
python3 .specify/scripts/query_postgres.py --db metrics-pg --schema
```

They accept the same options and enforce the same read-only rules. Their `--list` output omits the
protocol line, because each handler serves exactly one protocol.

## 5. Server-family notes

**Apache Doris / SelectDB.** MySQL protocol on port 9030. Set `"protocol": "mysql"`. These front
ends often run without TLS, so `"ssl_disabled": true` is common. Some builds do not implement
`max_execution_time`; the skill tolerates that and still enforces read-only access mode.

**ClickHouse.** PostgreSQL protocol on port 9005, not the native 9000 port. Set
`"protocol": "postgres"`. The front end implements a subset of PostgreSQL, so prefer plain
`SELECT` statements over `information_schema` exploration; `--tables` and `--schema` may return
little or fail on a given build. A missing `statement_timeout` setting is tolerated.

**MariaDB.** Behaves as MySQL. Older versions lack `max_execution_time`, which is tolerated.

## 6. What the skill refuses

Refusals happen before a connection is opened, and each exits 1 with a one-line reason:

- A statement whose first keyword is not a read keyword. Accepted leads are `SELECT`, `SHOW`,
  `DESCRIBE`, `EXPLAIN`, `WITH` and `DESC` on the MySQL family; the PostgreSQL family accepts the
  same set minus `DESC` plus the psql `\D` meta-command.
- `INTO OUTFILE` or `INTO DUMPFILE` anywhere in a MySQL-family statement — these write a file on
  the server, which read-only access mode does not cover.
- More than one statement. A semicolon anywhere except the trailing terminator is refused, so
  `SELECT 1; DROP TABLE t` is rejected as a whole.
- An entry missing `name`, `host`, `database`, `user` or `password`.
- An unknown `protocol` or `sslmode` value.

A leading keyword is a screen, not a proof: `WITH x AS (...) DELETE ...` starts with a read keyword
and passes the client check. That is exactly why the session is also put into read-only access mode
on the server, which refuses the write. Both layers are always applied.

## 7. When something fails

| Message | What to do |
|---------|------------|
| `Config not found. Searched:` | Create the registry, or pass `--config` |
| `Database '<name>' not found.` | Compare against `--list`; matching ignores case but not spelling |
| `Database config missing fields:` | Add the listed fields to that entry |
| `Error: Unknown protocol` | Use `mysql` or `postgres` |
| `Error: Handler not found` | Restore the handler file beside `query.py` |
| `Only read-only queries ... are allowed` | Rephrase as a read; this skill does not write |
| `Multiple statements not allowed` | One statement per invocation |
| `Authentication failed. Check credentials in connections.json` | Fix `user` / `password`; the real server text is withheld on purpose |
| `Database error: ...` | Read the server message; timeouts point at host/port/firewall, TLS errors at the settings above |
| `PyMySQL not installed` / `pg8000 not installed` | Install the driver named in the message |

Exit codes are 0 for a completed run, 1 for a documented failure, and 2 for a rejected command
line. An undeclared option is refused before any connection or file access.
