---
name: database-utils
description: |
  Execute read-only SQL queries against MySQL and PostgreSQL protocol databases.
  Supports MySQL, PostgreSQL, ClickHouse (PostgreSQL wire protocol), and Apache Doris/SelectDB (MySQL protocol).
  Use when: querying databases, exploring schemas/tables, running SELECT queries for data analysis,
  checking database contents.
  Triggers: "MySQL", "PostgreSQL", "database", "SQL", "query", "ClickHouse", "Doris", "SelectDB",
  "数据库", "查询", "SQL查询", "数据库查询", "表结构", "数据分析"
skill_id: "<SKILL:.specify/skills/database-utils/SKILL.md>"
license: MIT
metadata:
  author: spec-kit project
  version: "3.0"
classification: external
---

# Database Utilities

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Overview

This skill answers questions about data that lives in a relational server. It reads a registry of
connections, picks the entry the caller named, works out which wire protocol that entry speaks, and
runs one statement whose result is printed as a plain-text table. The deliverable is the query
result: the skill writes nothing outside its own connection file, and it never issues a statement
that could change data.

Read-only is enforced twice, on purpose. The statement is screened in the client before it is sent,
and the server session is then switched to read-only access mode, so a statement that the screen
admits but that would still write is refused by the server. Neither layer is a substitute for the
other, and neither is optional.

Three entry points share one command surface:

- `scripts/query.py` — the dispatcher. Resolves the entry and routes to a protocol handler.
- `scripts/query_mysql.py` — the MySQL-protocol handler, also usable on its own.
- `scripts/query_postgres.py` — the PostgreSQL-protocol handler, also usable on its own.

## Reachable Servers

| Server | Protocol value | Usual port |
|--------|----------------|------------|
| MySQL | `mysql` | 3306 |
| MariaDB | `mysql` | 3306 |
| Apache Doris / SelectDB | `mysql` | 9030 |
| PostgreSQL | `postgres` | 5432 |
| ClickHouse (PostgreSQL front end) | `postgres` | 9005 |

A server belongs to a protocol family, not to a product name: anything that answers the MySQL wire
protocol is reached with `mysql`, anything that answers the PostgreSQL wire protocol with `postgres`.

## Command Surface

Every entry point accepts the same options.

| Option | Meaning |
|--------|---------|
| `--list` | Print each configured entry with its protocol, host, database and description |
| `--db <name>`, `-d <name>` | Select an entry by name; matching ignores case |
| `--tables`, `-t` | List the tables of the selected database |
| `--schema`, `-s` | List the columns of the selected database with types and nullability |
| `--query "<sql>"`, `-q "<sql>"` | Run one read-only statement |
| `--limit <n>`, `-l <n>` | Cap the rows returned, unless the statement already carries a `LIMIT` |
| `--config <path>`, `-c <path>` | Read the registry from an explicit file instead of searching |
| `-h`, `--help` | Print the option vocabulary, the side-effect statement and the exit codes |
| `--version` | Print the script name and the framework version |

Mode precedence is `--list`, then `--tables`, then `--schema`, then `--query`. An undeclared option
is rejected before anything runs. The flag surface answers even when no database driver is
installed, so `--help`, `--version` and `--list` never depend on a reachable server.

## Requirements

- Python 3.8 or newer.
- `PyMySQL` (MIT) for the MySQL protocol family.
- `pg8000` (BSD-3-Clause) for the PostgreSQL protocol family.

```bash
pip install -r ${SKILL_HOME}/requirements.txt
```

Only the driver for the protocol actually queried has to be present. A missing driver is reported
with its install command when a connection is attempted, not at start-up.

## Setup

1. Create the registry from the shipped example:

```bash
cp ${SKILL_HOME}/connections.example.json ${SKILL_HOME}/connections.json
```

2. Replace the example entries with the servers to reach. Give each entry a `description` that says
   what data it holds — that field is what makes intent-based selection possible later.

3. Restrict the file, because it holds credentials:

```bash
chmod 600 ${SKILL_HOME}/connections.json
```

The dispatcher looks for the registry in this order and uses the first file that exists:

1. `${SKILL_HOME}/connections.json`
2. `${HOME}/.config/claude/db-connections.json`

The two standalone handlers search the same first location and then their own protocol-specific
file: `mysql-connections.json` for `query_mysql.py`, `postgres-connections.json` for
`query_postgres.py`, both under `${HOME}/.config/claude/`. A file that group or other can read
produces a warning naming the `chmod 600` repair; the warning does not stop the run.

## Connection Entry Fields

Shared by both protocols:

| Field | Required | Default | Meaning |
|-------|----------|---------|---------|
| `name` | yes | — | Entry identifier; lookup ignores case |
| `description` | yes | — | What data the entry holds, used to match user intent |
| `host` | yes | — | Server host name |
| `database` | yes | — | Database or schema to attach to |
| `user` | yes | — | Login name |
| `password` | yes | — | Login password |
| `protocol` | no | resolved from the port | `mysql`, `postgres` or `postgresql` |
| `port` | no | 3306 / 5432 | Server port, by protocol |

MySQL-protocol entries additionally accept:

| Field | Default | Meaning |
|-------|---------|---------|
| `ssl_disabled` | `false` | `true` connects without TLS |
| `ssl_ca` | — | CA certificate file |
| `ssl_cert` | — | Client certificate file |
| `ssl_key` | — | Client private key file |

PostgreSQL-protocol entries additionally accept `sslmode` (default `prefer`), with the libpq
vocabulary `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full`.

`require` encrypts without authenticating the peer; `verify-ca` also validates the certificate
chain; `verify-full` validates the chain and the host name. Wherever the server certificate can be
validated, choose `verify-full`, or `verify-ca` with a CA bundle scoped to that server — the
unverified modes exist for hosts with a private CA and are a per-entry choice, never a default
imposed on the whole registry.

## Protocol Resolution

The dispatcher decides in three steps, stopping at the first that answers:

1. An explicit `protocol` value, folded to lower case. `postgresql` is accepted as `postgres`.
   Any other value is an error naming the two supported families.
2. The port, when it is one of the known front-end ports in the table above.
3. `mysql` as the fallback.

State `protocol` explicitly for any server on a non-default port; inference is a convenience for
the standard ports, not a detection mechanism.

## Usage

```bash
# What is configured, and over which protocol
python3 ${SKILL_HOME}/scripts/query.py --list

# Structure of one database
python3 ${SKILL_HOME}/scripts/query.py --db production --tables
python3 ${SKILL_HOME}/scripts/query.py --db production --schema

# One statement, with a row cap
python3 ${SKILL_HOME}/scripts/query.py --db production --query "SELECT * FROM users" --limit 100

# An explicit registry file
python3 ${SKILL_HOME}/scripts/query.py --config /path/to/connections.json --db production --tables

# A protocol handler on its own
python3 ${SKILL_HOME}/scripts/query_mysql.py --db mysql-prod --tables
python3 ${SKILL_HOME}/scripts/query_postgres.py --db pg-analytics --schema
```

`--tables` and `--schema` are ordinary read-only statements against `information_schema`, so they
obey the same screening, the same row cap and the same rendering as `--query`. The MySQL variants
report the current database; the PostgreSQL variants report every non-system schema.

## Choosing the Right Database

When the request names a topic rather than an entry, match the topic against each entry's
`description`:

| The request is about | Look for a description mentioning |
|----------------------|-----------------------------------|
| people, accounts | users, accounts, customers |
| purchases, revenue | orders, transactions, sales |
| measurements, reporting | analytics, metrics, reports |
| incidents, activity | logs, events, audit |
| large-scale aggregation | warehouse, OLAP, data lake |

If more than one entry fits, run `--list` and ask which one to use rather than guessing.

## Read-only Enforcement

Client side, before a connection is opened:

- The statement must begin with a read keyword. MySQL protocol: `SELECT`, `SHOW`, `DESCRIBE`,
  `EXPLAIN`, `WITH`, `DESC`. PostgreSQL protocol: `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`, `WITH`,
  and the psql `\D` meta-command.
- MySQL protocol additionally refuses `INTO OUTFILE` and `INTO DUMPFILE`, which write a file on the
  server and are not covered by read-only access mode.
- One statement per invocation. A semicolon anywhere other than the trailing terminator is
  refused, so `SELECT 1; DROP TABLE t` never reaches a server.
- A row cap is appended only when the statement does not already contain `LIMIT <number>`.

Server side, on every connection:

- MySQL protocol: `SET SESSION TRANSACTION READ ONLY`, then a best-effort
  `max_execution_time` of 30 s (older servers that lack the variable are tolerated).
- PostgreSQL protocol: session characteristics set to read-only transactions, then a best-effort
  `statement_timeout` of 30 s (a compatible front end that lacks the setting is tolerated).
- Both: a 10 s connection timeout, and the connection is closed even when the statement fails.

The read-only session setting is never optional. Only the timeout is best effort, because a
missing timeout is a performance concern while a missing read-only mode is a safety one.

## Result Shape

Results print as a fixed-width table: a header row of column names, a rule of dashes, one line per
row, then a blank line and `(N rows)`.

- Values are rendered with `str()`; SQL `NULL` prints as `<NULL>`.
- A column is at most 100 characters wide; a longer value is cut to 97 characters plus `...`.
- At most 10,000 rows are fetched. When the fetch returns exactly that many, the footer adds
  `[truncated at 10000]` — treat the result as incomplete and narrow the statement.
- A statement that returns no result set prints `Query executed (no result set returned)`.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | The run completed, including a `--list`, `--help` or `--version` invocation |
| 1 | A documented check failed: no registry, unknown entry or protocol, missing entry field, refused statement, driver absent, or a server error |
| 2 | The command line itself was rejected (undeclared option or malformed argument) |

Server errors print as `Database error: <message>`. A message that mentions a password or an
authentication failure is replaced by a fixed hint pointing at the registry, so credentials never
reach the output.

## Troubleshooting

| Symptom | Repair |
|---------|--------|
| `Config not found. Searched:` | Create `connections.json` in the skill directory, or pass `--config` |
| `Database '<name>' not found.` | Run `--list`; the printed names are the accepted spellings |
| `Database config missing fields:` | Add the named fields to that entry |
| `Unknown protocol` | Set `protocol` to `mysql` or `postgres` |
| `Handler not found` | Keep `query_mysql.py` and `query_postgres.py` beside `query.py` |
| `Only read-only queries ... are allowed` | Rephrase as a read statement; writes are out of scope for this skill |
| `Multiple statements not allowed` | Run each statement as its own invocation |
| `Authentication failed.` | Correct `user` / `password` in the registry |
| Connection timeout | Check host, port, firewall and VPN reachability |
| MySQL TLS handshake failure | For a local server without TLS, set `"ssl_disabled": true` |
| PostgreSQL TLS handshake failure | Set `"sslmode": "disable"` for a local server, or supply a CA for `verify-ca` |
| `Unknown sslmode` | Use one of the six documented values |
| Insecure-permissions warning | `chmod 600 connections.json` |
| `PyMySQL not installed` / `pg8000 not installed` | `pip install -r ${SKILL_HOME}/requirements.txt` |
| Result ends with `[truncated at 10000]` | Add a filter or a smaller `LIMIT` |

## Workflow

1. `--list` to see the entries and their protocols.
2. Match the request to one entry by its description; ask when the match is ambiguous.
3. `--tables`, then `--schema`, to learn the structure before writing SQL.
4. Run the statement with a row cap appropriate to the question.
5. Report the result, and say so explicitly when the footer marks it truncated.

## Path Conventions

- `${SKILL_HOME}` — the directory holding this SKILL.md.
- `${SKILL_WORKDIR}` — the caller's working directory at invocation time.

Every script path above is written against `${SKILL_HOME}` so the skill stays portable.

## Resources

- `scripts/query.py` — dispatcher: entry selection and protocol routing.
- `scripts/query_mysql.py` — MySQL-protocol handler.
- `scripts/query_postgres.py` — PostgreSQL-protocol handler.
- `references/setup-and-usage.md` — installation, registry authoring and worked invocations.
- `connections.example.json` — one example entry per reachable server family.
- `requirements.txt` — the two drivers.
- `LICENSE.txt` — MIT license for this skill.

## Dependencies

- `PyMySQL` — MySQL wire protocol driver (MIT).
- `pg8000` — PostgreSQL wire protocol driver (BSD-3-Clause).

Both are pure Python and need no compiler or system client library.

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 2845f5641171 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:database-utils" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:database-utils" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:database-utils" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
