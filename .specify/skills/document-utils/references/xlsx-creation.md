# Creating, Editing and Checking Workbooks

[openpyxl](https://openpyxl.readthedocs.io/) (MIT) reads and writes `.xlsx`. It
handles cells, styles, formulas, charts and sheets; it does **not** evaluate
formulas. That single limitation shapes the whole workflow below: a script writes
the formula, and a spreadsheet engine calculates it.

```bash
python -m pip install openpyxl
```

## The rule that matters most: write formulas, not results

A workbook is a model, not a report. When a cell is derived from other cells, put
the derivation in the cell so a reader can change an input and see the effect.
Computing the number in Python and writing the result produces a file that looks
right and is dead.

```python
# Wrong: the spreadsheet cannot recalculate any of these
ws["B10"] = sum(revenue)                       # a total that will not follow the rows
ws["C5"] = (this_year - last_year) / last_year  # a growth rate frozen at build time
ws["D8"] = statistics.mean(scores)              # an average that ignores later edits

# Right: the model stays live
ws["B10"] = "=SUM(B2:B9)"
ws["C5"] = "=(B5-B4)/B4"
ws["D8"] = "=AVERAGE(D2:D7)"
```

Hardcode only what is genuinely an input: an assumption, a published figure, a
price. Everything derived from those is a formula. See
[xlsx-financial-models.md](./xlsx-financial-models.md) for how inputs and
formulas are marked so a reader can tell them apart.

## Creating a workbook

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Model"

ws["A1"] = "Revenue"
ws["B1"] = 1000                     # an input
ws["B2"] = "=B1*1.05"               # a projection
ws["B3"] = "=SUM(B1:B2)"

ws["A1"].font = Font(name="Arial", size=11, bold=True)
ws["B1"].font = Font(name="Arial", color="0000FF")        # blue = hardcoded input
ws["B1"].number_format = '"$"#,##0;("$"#,##0);"-"'
ws["B2"].number_format = "0.0%"
ws["B1"].fill = PatternFill("solid", start_color="FFFF00")  # needs attention
ws["B1"].alignment = Alignment(horizontal="right")
ws["B1"].border = Border(bottom=Side(style="thin", color="999999"))
ws["B1"].comment = Comment("Source: annual report 2025, page 42", "model")

ws.column_dimensions["A"].width = 28
ws.freeze_panes = "B2"

wb.save("output.xlsx")
```

Cell addresses are 1-based: `ws.cell(row=1, column=1)` is `A1`.
`openpyxl.utils.get_column_letter` converts an index to letters -- 27 is `AA`,
64 is `BL`. Off-by-one in a column index is the most common reference bug in a
generated model, so convert rather than count by hand.

## Reading and analysing

```python
wb = openpyxl.load_workbook("output.xlsx", data_only=True)
ws = wb["Model"]

for row in ws.iter_rows(min_row=2, values_only=True):
    label, value = row[0], row[1]
    ...

print(ws["B3"].value)          # the cached result, or None if nothing calculated it
print(ws.max_row, ws.max_column)
```

Two loading modes, two different things:

| Mode | `cell.value` for a formula cell |
|------|---------------------------------|
| `data_only=False` (default) | the formula text, e.g. `"=SUM(B1:B2)"` |
| `data_only=True` | the last cached result, or `None` if there is none |

**Never save a workbook loaded with `data_only=True`.** The formulas are not in
that object; saving replaces every formula with its cached value, permanently.
Load with `data_only=True` to read, and keep a separate default-mode load for any
write.

For a large file, stream it:

```python
wb = openpyxl.load_workbook("big.xlsx", read_only=True)
for row in wb["Sheet"].iter_rows(values_only=True):
    ...
wb.close()
```

`read_only=True` does not load the whole sheet into memory; `write_only=True` is
its counterpart for building one. Neither supports random access to cells.

## Editing an existing workbook

```python
wb = openpyxl.load_workbook("template.xlsx")      # default mode: formulas preserved
ws = wb["Inputs"]
ws["B4"] = 0.07                                   # change an assumption
ws["B5"] = "=B4*1.1"                              # add a formula

extra = wb.create_sheet("Scenario")
extra["A1"] = "=Inputs!B4"                        # cross-sheet reference
wb.save("template-updated.xlsx")
```

Match the file's existing conventions -- its fonts, its number formats, its
colour coding, its layout. An established template outranks any general guidance,
including this file's.

## Recalculating formulas

A workbook written by openpyxl has formulas and no cached values, so Excel shows
the results but a script reading `data_only=True` sees `None`. Recalculation fills
those values in:

```bash
python ${SKILL_HOME}/scripts/xlsx/recalc.py output.xlsx          # 30 s budget
python ${SKILL_HOME}/scripts/xlsx/recalc.py output.xlsx 60       # a longer one
```

What the script does:

1. Installs a small StarBasic macro in the LibreOffice user profile on first run
   (an existing module is never overwritten; the sub is appended to it).
2. Runs LibreOffice headless against the file. The macro calls `calculateAll()`
   and stores the document, so the formulas stay and the cached values appear.
3. Reads the saved file twice with openpyxl: once for values, to find cells that
   evaluated to an error, and once for formulas, to count them.
4. Prints a JSON verdict on stdout.

LibreOffice must be installed and on `PATH`. The exit code is 0 for a verdict --
including one that reports errors -- and 1 only for a missing operand or a
non-integer timeout. Read the verdict from the JSON, not from the exit status.

### The verdict

```json
{
  "status": "errors_found",
  "total_errors": 2,
  "error_summary": {
    "#DIV/0!": {"count": 1, "locations": ["Model!B7"]},
    "#REF!": {"count": 1, "locations": ["Model!C12"]}
  },
  "total_formulas": 42
}
```

| Field | Meaning |
|-------|---------|
| `status` | `success` when no cell holds an error value, otherwise `errors_found` |
| `total_errors` | number of cells holding an error value |
| `total_formulas` | number of formula cells in the workbook |
| `error_summary` | per error type: the full `count` and up to 20 `Sheet!Cell` locations |

A run that could not start prints `{"error": "..."}` instead -- a missing file, a
profile that could not be initialized, or a LibreOffice failure. A timeout is not
automatically a failure: the macro stores the document before closing it, so the
scan still reads whatever reached the disk.

The error values it looks for:

| Token | Usual cause |
|-------|-------------|
| `#VALUE!` | an operand of the wrong type -- text where a number belongs |
| `#DIV/0!` | a denominator that is zero or empty |
| `#REF!` | a reference to a cell that was deleted |
| `#NAME?` | a function or name the engine does not know |
| `#NULL!` | an intersection of ranges that do not intersect |
| `#NUM!` | a number outside what the function accepts |
| `#N/A` | a lookup that found no match |

`#N/A` from a lookup is sometimes intentional. Everything else is a defect: a
delivered model has zero formula errors.

## Verification checklist

Before calling a workbook finished:

- [ ] Recalculated, and `status` is `success`.
- [ ] Two or three references spot-checked against the cells they should pull.
- [ ] Column letters converted, not counted (`get_column_letter`).
- [ ] Row offsets accounted for: a header in row 1 means data starts at row 2.
- [ ] Every denominator guarded, or proven non-zero (`=IF(B2=0,"",A2/B2)`).
- [ ] Ranges cover exactly the intended rows -- no off-by-one at either end.
- [ ] The same formula pattern across every period of a projection.
- [ ] Cross-sheet references spelled `Sheet!A1`, with quotes when the name has a
      space: `'FY 2026'!B4`.
- [ ] No unintended circular reference.
- [ ] Edge cases tried: zero, negative, empty, and a very large value.
- [ ] Every hardcode carries a source comment.

Start small: build two or three formulas, recalculate, check them, then extend
the pattern. A mistake repeated across four hundred cells is four hundred fixes.

## Other things openpyxl does

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.chart import BarChart, Reference

ws.conditional_formatting.add(
    "B2:B20", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="FF0000"))
)
wb.defined_names.add(DefinedName("GrowthRate", attr_text="Model!$B$1"))

chart = BarChart()
chart.add_data(Reference(ws, min_col=2, min_row=1, max_row=13), titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=2, max_row=13))
ws.add_chart(chart, "E2")
```

A named range makes a model readable (`=Revenue*GrowthRate`) and survives row
insertion, which a bare address does not.

## Pitfalls

- **Saving a `data_only=True` load.** Formulas are gone for good.
- **Expecting openpyxl to calculate.** It writes formula text; only an engine
  evaluates it. Recalculate before reading values.
- **A cached value that is stale.** After editing a formula, the old cached value
  stays until the next recalculation. Recalculate after every edit, not once at
  the end of a long session.
- **`ws.max_row` after deletions.** It reflects the sheet's dimension record,
  which can lag behind the cells you removed.
- **Merged cells.** Only the top-left cell holds the value; writing to another
  cell of a merged range raises or is silently ignored.
- **Dates.** openpyxl returns `datetime` objects; a number format decides how they
  display. Writing a string where a date belongs breaks every date formula.
- **Styles are per cell.** There is no "apply to column" shortcut; loop, or use a
  named style.

## Code style

Keep the generating code short: no redundant prints, no ceremony. Put the
explanation where a reader of the *workbook* will find it -- a cell comment on a
complex formula, a source note beside a hardcode, a label above each block of the
model.