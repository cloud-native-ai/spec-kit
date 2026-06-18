# Data Model: Skill Directory Layout

**Spec**: `017-consolidate-draft-skills` | **Date**: 2026-06-18

This document defines the target directory structure for each consolidated skill. These are file-system entities (directories and files), not database entities.

## Entity: document-utils

```text
skills/document-utils/
├── SKILL.md                    # Unified skill definition (hub + format sections)
├── LICENSE.txt                 # Proprietary license (from docx/pdf/pptx/xlsx-utils)
├── scripts/
│   ├── office/                 # Shared Office tooling (ONE copy, deduplicated)
│   │   ├── soffice.py          # LibreOffice automation wrapper
│   │   ├── pack.py             # XML → OOXML repackaging
│   │   ├── unpack.py           # OOXML → XML extraction
│   │   ├── validate.py         # OOXML validation
│   │   ├── helpers/
│   │   │   ├── __init__.py
│   │   │   ├── merge_runs.py
│   │   │   └── simplify_redlines.py
│   │   └── validators/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── docx.py
│   │       ├── pptx.py
│   │       └── redlining.py
│   ├── docx/                   # DOCX-specific scripts
│   │   ├── accept_changes.py
│   │   ├── comment.py
│   │   ├── __init__.py
│   │   └── templates/          # XML templates for comments
│   │       ├── commentsExtended.xml
│   │       ├── commentsExtensible.xml
│   │       ├── commentsIds.xml
│   │       ├── comments.xml
│   │       └── people.xml
│   ├── pdf/                    # PDF-specific scripts
│   │   ├── check_bounding_boxes.py
│   │   ├── check_fillable_fields.py
│   │   ├── convert_pdf_to_images.py
│   │   ├── create_validation_image.py
│   │   ├── extract_form_field_info.py
│   │   ├── extract_form_structure.py
│   │   ├── fill_fillable_fields.py
│   │   └── fill_pdf_form_with_annotations.py
│   ├── pptx/                   # PPTX-specific scripts
│   │   ├── add_slide.py
│   │   ├── clean.py
│   │   ├── __init__.py
│   │   └── thumbnail.py
│   └── xlsx/                   # XLSX-specific scripts
│       └── recalc.py
├── references/
│   ├── pdf-forms.md            # PDF form filling guide (from pdf-utils/forms.md)
│   ├── pdf-reference.md        # Advanced PDF reference (from pdf-utils/reference.md)
│   ├── pptx-editing.md         # PPTX editing guide (from pptx-utils/editing.md)
│   └── pptx-creation.md        # PptxGenJS guide (from pptx-utils/pptxgenjs.md)
└── themes/
    ├── theme-showcase.pdf      # Visual theme gallery
    ├── arctic-frost.md
    ├── botanical-garden.md
    ├── desert-rose.md
    ├── forest-canopy.md
    ├── golden-hour.md
    ├── midnight-galaxy.md
    ├── modern-minimalist.md
    ├── ocean-depths.md
    ├── sunset-boulevard.md
    └── tech-innovation.md
```

### Key Design Decisions

- **Shared `scripts/office/`**: docx-utils, pptx-utils, and xlsx-utils all contained identical copies of the `scripts/office/` directory. Consolidated into a single copy. Format-specific scripts are organized under `scripts/<format>/`.
- **References directory**: Reference docs from individual draft skills (forms.md, reference.md, editing.md, pptxgenjs.md) are moved to `references/` with prefixed names for disambiguation.
- **Themes directory**: The entire `themes/` directory from theme-creator moves directly into document-utils, including the visual showcase PDF.
- **License**: All 5 source skills use the same proprietary license. One LICENSE.txt is sufficient.

---

## Entity: database-utils

```text
skills/database-utils/
├── SKILL.md                    # Unified skill definition (MySQL + PostgreSQL sections)
├── LICENSE.txt                 # Apache-2.0 license
├── connections.example.json    # Unified example with protocol field
├── requirements.txt            # Combined Python dependencies
├── .gitignore                  # Ignore connections.json
├── scripts/
│   ├── query.py                # Unified query script with protocol dispatch
│   └── query_mysql.py          # MySQL-specific query logic (from mysql-utils/scripts/query.py)
│   └── query_postgres.py       # PostgreSQL-specific query logic (from postgres-utils/scripts/query.py)
└── references/
    └── README.md               # Consolidated setup and usage guide
```

### Key Design Decisions

- **Unified `connections.example.json`**: Adds a `protocol` field (`"mysql"` or `"postgres"`) to each connection entry. If absent, protocol is inferred from port (3306→mysql, 5432→postgres).
- **Script architecture**: A unified `query.py` entry point that dispatches to `query_mysql.py` or `query_postgres.py` based on the connection's protocol. This preserves the distinct driver logic while presenting a single command interface.
- **Combined `requirements.txt`**: Merges `mysql-connector-python` and `psycopg2-binary` into one file.
- **License**: Both source skills use Apache-2.0.

### Connection Configuration Schema

```json
{
  "databases": [
    {
      "name": "string (required)",
      "description": "string (required)",
      "protocol": "mysql | postgres (optional, inferred from port if absent)",
      "host": "string (required)",
      "port": "integer (optional, default: 3306 for mysql, 5432 for postgres)",
      "database": "string (required)",
      "user": "string (required)",
      "password": "string (required)",
      "ssl_disabled": "boolean (optional, MySQL only)",
      "ssl_ca": "string (optional, MySQL only)",
      "ssl_cert": "string (optional, MySQL only)",
      "ssl_key": "string (optional, MySQL only)",
      "sslmode": "string (optional, PostgreSQL only: disable|allow|prefer|require|verify-ca|verify-full)"
    }
  ]
}
```

### Supported Database Systems

| Database | Protocol | Default Port | Notes |
|----------|----------|-------------|-------|
| MySQL | mysql | 3306 | Native MySQL protocol |
| PostgreSQL | postgres | 5432 | Native PostgreSQL protocol |
| ClickHouse | postgres | 9005 | PostgreSQL wire protocol interface |
| Apache Doris / SelectDB | mysql | 9030 | MySQL protocol compatible |

---

## Entity: browser-utils

```text
skills/browser-utils/
├── SKILL.md                    # Unified skill definition (JS automation + Python testing)
├── LICENSE.txt                 # Proprietary license (from web-test)
├── scripts/
│   ├── js/                     # JavaScript automation (from playwright-utils)
│   │   ├── run.js              # Universal Playwright executor
│   │   ├── package.json        # Node.js dependencies
│   │   └── lib/                # Helper library (if present in playwright-utils)
│   └── python/                 # Python testing (from web-test)
│       └── with_server.py      # Server lifecycle manager
├── references/
│   └── playwright-api.md       # Playwright API reference (from playwright-utils/API_REFERENCE.md)
└── examples/                   # Python examples (from web-test/examples)
    ├── console_logging.py
    ├── element_discovery.py
    └── static_html_automation.py
```

### Key Design Decisions

- **Language-separated scripts**: JavaScript automation files under `scripts/js/`, Python testing under `scripts/python/`. This avoids conflating two different execution environments.
- **Examples preserved**: The web-test examples are useful learning material and are preserved in `examples/`.
- **API reference**: The comprehensive Playwright API reference from playwright-utils moves to `references/`.
- **License**: Uses the proprietary license from web-test. playwright-utils had no license file.

---

## File Count Summary

| Skill | SKILL.md | Scripts | References | Other | Total Files |
|-------|----------|---------|------------|-------|-------------|
| document-utils | 1 | ~25 | 4 | 12 (themes + license) | ~42 |
| database-utils | 1 | 3 | 1 | 4 (config, requirements, gitignore, license) | ~9 |
| browser-utils | 1 | 3 | 1 | 4 (examples + license) | ~9 |
| **Total** | **3** | **~31** | **6** | **~20** | **~60** |
