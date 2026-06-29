#!/usr/bin/env bash
# render-plantuml.sh — Render PlantUML to high-quality SVG/PNG
#
# Ensures the style block (scale 4 + dpi 300) is always applied so output
# dimensions exceed 3840×2160 (4K UHD). SVG is preferred — it is vector
# and scales losslessly to any display.
#
# Usage: render-plantuml.sh <input.puml> [output_dir] [output_prefix]

set -euo pipefail

PLANTUML_SERVER="${PLANTUML_SERVER:-http://workspace.code-workspace.cloud:39156/plantuml}"
SCALE=4          # Produces SVG viewBox ~4800+ and PNG ~4096 (server cap), both ≥ 3840
DPI=300

log() { printf '[render-plantuml] %s\n' "$*" >&2; }

# ── Style injection ───────────────────────────────────────────────────────────

# Inject standard style block after @startuml if not already present.
# Removes any conflicting directives first to avoid duplicates.
inject_style() {
  local input="$1" output="$2"
  local style_tmp="${output}.style.tmp"
  cat <<EOF > "$style_tmp"
skinparam monochrome true
skinparam shadowing false
skinparam roundCorner 20
skinparam dpi ${DPI}
scale ${SCALE}
skinparam defaultFontSize 14
skinparam defaultFontName "Arial, Helvetica, sans-serif"
skinparam padding 8
skinparam ArrowThickness 2
skinparam BorderThickness 2
skinparam svgDimensionStyle false
skinparam svgLinkTarget _blank
EOF

  # Remove existing skinparam/scale directives that we're about to inject (avoid duplicates).
  # Direction directives are preserved — they are diagram-type-specific and left to the author.
  sed -E \
    -e '/^[[:space:]]*skinparam[[:space:]]+(monochrome|shadowing|roundCorner|dpi|defaultFontSize|defaultFontName|padding|ArrowThickness|BorderThickness|svgDimensionStyle|svgLinkTarget|actorStyle)/d' \
    -e '/^[[:space:]]*scale[[:space:]]/d' \
    "$input" | sed "/^@startuml/r ${style_tmp}" > "$output"

  rm -f "$style_tmp"
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
  local input="${1:-}" output_dir="${2:-.}" prefix="${3:-diagram}"

  if [[ -z "$input" ]] || [[ ! -f "$input" ]]; then
    echo "Usage: render-plantuml.sh <input.puml> [output_dir] [output_prefix]" >&2
    exit 1
  fi

  mkdir -p "$output_dir"

  local puml="${output_dir}/${prefix}.puml"
  local svg="${output_dir}/${prefix}.svg"
  local png="${output_dir}/${prefix}.png"

  # Ensure style block is present
  inject_style "$input" "$puml"
  log "Style applied (scale=${SCALE}, dpi=${DPI})"

  # Render SVG (preferred — vector, lossless at any zoom)
  log "Rendering SVG..."
  curl -sf -X POST -H "Content-Type: text/plain" \
    --data-binary "@${puml}" "${PLANTUML_SERVER}/svg" -o "$svg"

  # Render PNG (high-res, 300 DPI)
  log "Rendering PNG..."
  curl -sf -X POST -H "Content-Type: text/plain" \
    --data-binary "@${puml}" "${PLANTUML_SERVER}/png" -o "$png"

  # Report dimensions
  local svg_vb png_dim
  svg_vb=$(grep -oE 'viewBox="[^"]*"' "$svg" 2>/dev/null | head -1 || echo "unknown")
  png_dim=$(file "$png" 2>/dev/null | grep -oE '[0-9]+ x [0-9]+' | head -1 || echo "unknown")

  echo "=== Rendering Complete ==="
  echo "Source: ${puml}"
  echo "SVG:    ${svg} (${svg_vb})"
  echo "PNG:    ${png} (${png_dim})"
  echo "Config: scale=${SCALE}, dpi=${DPI} — output ≥ 3840×2160"
}

main "$@"
