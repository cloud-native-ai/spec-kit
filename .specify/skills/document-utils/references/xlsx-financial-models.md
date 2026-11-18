# Standards for Financial Models in Excel

A model is read by someone who has to trust it without rebuilding it. These
conventions exist so that a reader can tell, at a glance, what is an input, what
is a calculation, and where a number came from.

When the file being edited already has conventions, **the file wins**. Match its
fonts, its colours, its formats and its layout exactly; do not impose this page
on a template that has its own language.

## Every workbook

- **One professional font throughout.** Arial or Times New Roman at 10-12 pt
  unless the user or the template says otherwise. Mixed fonts read as mixed
  provenance.
- **Zero formula errors on delivery.** `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`,
  `#NUM!`, `#NULL!` are defects. Run
  `python ${SKILL_HOME}/scripts/xlsx/recalc.py model.xlsx` and read the verdict;
  `status` must be `success`. An intentional `#N/A` from a lookup is documented in
  a comment, not left unexplained.
- **Units in the header, not in the cell.** `Revenue ($mm)` or `Revenue (EUR k)`
  once, above the column. A number formatted with a currency symbol in every cell
  cannot be aggregated cleanly and hides the scale.
- **A source for every hardcode.** See the last section.

## Colour coding

The convention is decades old and reads the same in every bank and every fund.
Colour marks the *role* of a cell, not its importance.

| Role | Font colour | Hex | Meaning |
|------|-------------|-----|---------|
| Hardcoded input | blue | `0000FF` | a number someone may change: an assumption, a published figure, a scenario lever |
| Formula | black | `000000` | everything calculated inside this sheet |
| Link from another sheet in this workbook | green | `008000` | `='Inputs'!B4` |
| Link to another file | red | `FF0000` | an external dependency; flag it, because it breaks when the file moves |
| Needs attention | yellow fill | `FFFF00` | an assumption to confirm, a placeholder to replace, a cell the reader must update |

```python
from openpyxl.styles import Font, PatternFill

ws["B4"].font = Font(name="Arial", color="0000FF")            # input
ws["B5"].font = Font(name="Arial", color="000000")            # formula
ws["B6"].font = Font(name="Arial", color="008000")            # cross-sheet link
ws["B7"].fill = PatternFill("solid", start_color="FFFF00")    # confirm this
```

Blue is the signal that matters most: a reader changes blue cells and trusts
black ones. A hardcoded number left in black is a trap, because it looks
calculated and will not follow the model.

## Number formats

| Quantity | Format | Note |
|----------|--------|------|
| Year | text (`"2026"`) | a year is a label; `2,026` is wrong and `2026` as a number invites arithmetic |
| Currency | `$#,##0` | scale stated in the header |
| Zero | `-` | third section of the format string |
| Negative | parentheses | `(1,234)`, not `-1,234` |
| Percentage | `0.0%` | one decimal unless precision is the point |
| Multiple | `0.0"x"` | EV/EBITDA, P/E |
| Date | `dd-mmm-yyyy` | unambiguous across locales |

A three-section format handles positive, negative and zero in one string:

```python
ws["B5"].number_format = '$#,##0;($#,##0);"-"'
ws["C5"].number_format = '0.0%;(0.0%);"-"'
ws["D5"].number_format = '0.0"x"'
```

Apply the zero-as-dash rule to percentages too. A column of `0.0%` values is
noise; a column of dashes lets the non-zero rows stand out.

## Formulas

**Assumptions live in their own cells.** Growth rates, margins, multiples, tax
rates, discount rates: one place, labelled, blue, referenced everywhere else.

```python
# Wrong: the assumption is buried in the arithmetic
ws["C10"] = "=B10*1.05"

# Right: the assumption is a cell someone can find and change
ws["B2"] = 0.05                      # labelled "Revenue growth", blue
ws["C10"] = "=B10*(1+$B$2)"
```

Absolute references (`$B$2`) for assumptions, relative references for the row's
own data. A projection filled across ten periods must use the same formula in
every period -- a pattern that changes halfway is either a deliberate step or a
bug, and the reader cannot tell which.

Guard the operations that can fail:

```python
ws["C5"] = "=IF(B5=0,\"\",A5/B5)"                 # division
ws["C6"] = "=IFERROR(VLOOKUP(A6,Rates!A:B,2,FALSE),0)"   # lookup, with a stated fallback
```

A fallback is a modelling decision, so document it in a comment rather than
letting `IFERROR` hide a broken reference.

Before delivery, check: every reference points where it should; ranges have no
off-by-one at either end; the pattern is identical across periods; zero,
negative and empty inputs were tried; no circular reference exists that was not
intended and iterative calculation enabled for.

## Documenting hardcodes

Every hardcoded number carries a source, in a cell comment or in the adjacent
cell at the end of a table. The form is: system or document, date, the specific
place inside it, and a link where one exists.

```
Source: Company 10-K, FY2025, p. 48, Revenue note, <EDGAR URL>
Source: Company 10-Q, Q2 2026, Exhibit 99.1, <EDGAR URL>
Source: Bloomberg Terminal, 2026-08-15, AAPL US Equity
Source: FactSet, 2026-08-20, Consensus Estimates screen
Source: Management interview, 2026-09-02, CFO, capacity plan
```

```python
from openpyxl.comments import Comment

ws["B4"].comment = Comment("Source: Company 10-K, FY2025, p. 48, Revenue note", "model")
```

A hardcode without a source is an assumption nobody approved. If the number
cannot be sourced, it is a placeholder: mark it yellow and say what is missing.

## Structure a reader can follow

- Inputs on their own sheet, or in one clearly labelled block at the top.
- Calculations below or beside the inputs, never interleaved with them.
- One row per period, one column per line item, consistent across every sheet.
- A check row or block that proves the model ties: balance sheet balances, cash
  flow reconciles, totals equal the sum of their parts. Make the check a formula
  that returns zero, and format a non-zero result so it cannot be missed.
- Labels in the leftmost column, units in the header, no merged cells inside a
  data range -- they break sorting, references and streaming reads.