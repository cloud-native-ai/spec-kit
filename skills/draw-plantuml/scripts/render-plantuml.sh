#!/usr/bin/env bash
# render-plantuml.sh — Render PlantUML to high-quality SVG and adaptive PNG
#
# SVG: Always rendered at scale 4 + dpi 300 (vector, no size limit).
# PNG: Adaptively calculates scale/dpi to fit within PNG_MAX (default 4095),
#      ensuring output is never blank due to server buffer overflow.
#
# The PlantUML server has a hard PNG dimension cap of 4096×4096. When the
# internal rendering buffer exceeds this, it silently returns a blank image.
# This script targets PNG_MAX (4095) to stay safely below the cap.
#
# Usage: render-plantuml.sh <input.puml> [output_dir] [output_prefix]

set -euo pipefail

PLANTUML_SERVER="${PLANTUML_SERVER:-http://workspace.code-workspace.cloud:39156/plantuml}"
SVG_SCALE=4        # SVG: maximum quality (vector, no size limit)
SVG_DPI=300
PNG_MAX=4095       # PNG: target max dimension (< server hard cap 4096)
PNG_DPI=300        # PNG: preferred DPI for high pixel density
PNG_MIN_DPI=96     # PNG: minimum DPI fallback
PNG_BLANK_THRESHOLD=100000  # PNG file size below this for 4096×4096 = likely blank

log() { printf '[render-plantuml] %s\n' "$*" >&2; }
warn() { printf '[render-plantuml] WARNING: %s\n' "$*" >&2; }

# ── Style injection ───────────────────────────────────────────────────────────

# Remove existing style directives that we'll inject (avoid duplicates).
# Direction directives (top to bottom, left to right) are preserved.
strip_style() {
  local input="$1"
  sed -E \
    -e '/^[[:space:]]*skinparam[[:space:]]+(monochrome|shadowing|roundCorner|dpi|defaultFontSize|defaultFontName|padding|ArrowThickness|BorderThickness|svgDimensionStyle|svgLinkTarget|actorStyle)/d' \
    -e '/^[[:space:]]*scale[[:space:]]/d' \
    "$input"
}

# Inject style block with given scale and dpi after @startuml.
inject_style() {
  local input="$1" output="$2" scale="$3" dpi="$4"
  local style_tmp="${output}.style.tmp"

  cat <<EOF > "$style_tmp"
skinparam monochrome true
skinparam shadowing false
skinparam roundCorner 20
skinparam dpi ${dpi}
scale ${scale}
skinparam defaultFontSize 14
skinparam defaultFontName "Arial, Helvetica, sans-serif"
skinparam padding 8
skinparam ArrowThickness 2
skinparam BorderThickness 2
skinparam svgDimensionStyle false
skinparam svgLinkTarget _blank
EOF

  strip_style "$input" | sed "/^@startuml/r ${style_tmp}" > "$output"
  rm -f "$style_tmp"
}

# ── PNG adaptive rendering ────────────────────────────────────────────────────

# Calculate optimal PNG scale and DPI from SVG viewBox dimensions.
# Target: max(width, height) ≤ PNG_MAX
#
# Relationship: PNG_pixels ≈ SVG_viewBox_at_target_scale
# So: target_scale = PNG_MAX / max(svg_w, svg_h) * SVG_SCALE
#
# If target_scale < 1, keep scale=1 and reduce DPI instead:
#   target_dpi = PNG_MAX * PNG_DPI / (max_dim / SVG_SCALE)
calc_png_params() {
  local svg_file="$1"
  local viewbox max_dim target_scale target_dpi

  # Extract viewBox dimensions from SVG
  viewbox=$(grep -oE 'viewBox="[0-9]+ [0-9]+ [0-9]+ [0-9]+"' "$svg_file" 2>/dev/null | head -1)
  if [[ -z "$viewbox" ]]; then
    # Fallback: can't parse viewBox, use safe defaults
    echo "2 150"
    return
  fi

  local vb_w vb_h
  vb_w=$(echo "$viewbox" | grep -oE '[0-9]+' | sed -n '3p')
  vb_h=$(echo "$viewbox" | grep -oE '[0-9]+' | sed -n '4p')

  if [[ -z "$vb_w" ]] || [[ -z "$vb_h" ]]; then
    echo "2 150"
    return
  fi

  # max dimension from SVG rendered at SVG_SCALE
  if (( vb_w > vb_h )); then
    max_dim=$vb_w
  else
    max_dim=$vb_h
  fi

  # Base dimension (at scale 1) = max_dim / SVG_SCALE
  local base_dim=$(( max_dim / SVG_SCALE ))

  # Calculate scale to fit within PNG_MAX at PNG_DPI
  # PNG size ≈ base_dim × scale × (dpi / 300)
  # At dpi 300: PNG size ≈ base_dim × scale
  # Want: base_dim × scale ≤ PNG_MAX
  # scale ≤ PNG_MAX / base_dim
  target_scale=$(( PNG_MAX / base_dim ))

  if (( target_scale >= SVG_SCALE )); then
    # Diagram is small enough for max scale at full DPI
    echo "${SVG_SCALE} ${PNG_DPI}"
  elif (( target_scale >= 1 )); then
    # Use reduced integer scale at full DPI
    echo "${target_scale} ${PNG_DPI}"
  else
    # Scale 1 still exceeds PNG_MAX at dpi 300
    # Reduce DPI: want base_dim × 1 × (dpi/300) ≤ PNG_MAX
    # dpi ≤ PNG_MAX × 300 / base_dim
    target_dpi=$(( PNG_MAX * PNG_DPI / base_dim ))
    if (( target_dpi < PNG_MIN_DPI )); then
      target_dpi=$PNG_MIN_DPI
    fi
    echo "1 ${target_dpi}"
  fi
}

# Validate PNG output is not blank/corrupted.
# Returns 0 if valid, 1 if likely blank.
validate_png() {
  local png_file="$1"
  local file_size dim_info

  if [[ ! -f "$png_file" ]]; then
    return 1
  fi

  file_size=$(wc -c < "$png_file" | tr -d ' ')

  # Check if file hit 4096 cap AND is suspiciously small (likely blank)
  dim_info=$(file "$png_file" 2>/dev/null)
  if echo "$dim_info" | grep -q "4096 x 4096" && (( file_size < PNG_BLANK_THRESHOLD )); then
    return 1
  fi

  # Also check for very small files that indicate rendering failure
  if (( file_size < 1000 )); then
    return 1
  fi

  return 0
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
  local png_puml="${output_dir}/${prefix}.png.tmp.puml"

  # ── Step 1: Render SVG (always at max quality) ──
  inject_style "$input" "$puml" "$SVG_SCALE" "$SVG_DPI"
  log "SVG style applied (scale=${SVG_SCALE}, dpi=${SVG_DPI})"

  log "Rendering SVG..."
  if ! curl -sf -X POST -H "Content-Type: text/plain" \
    --data-binary "@${puml}" "${PLANTUML_SERVER}/svg" -o "$svg"; then
    warn "SVG rendering failed"
    rm -f "$png_puml"
    exit 1
  fi

  # ── Step 2: Calculate optimal PNG parameters ──
  local png_params png_scale png_dpi
  png_params=$(calc_png_params "$svg")
  png_scale=$(echo "$png_params" | cut -d' ' -f1)
  png_dpi=$(echo "$png_params" | cut -d' ' -f2)
  log "PNG adaptive params: scale=${png_scale}, dpi=${png_dpi} (target ≤ ${PNG_MAX}px)"

  # ── Step 3: Render PNG with adaptive parameters ──
  inject_style "$input" "$png_puml" "$png_scale" "$png_dpi"

  log "Rendering PNG..."
  if ! curl -sf -X POST -H "Content-Type: text/plain" \
    --data-binary "@${png_puml}" "${PLANTUML_SERVER}/png" -o "$png"; then
    warn "PNG rendering failed"
    rm -f "$png_puml"
    exit 1
  fi

  # ── Step 4: Validate PNG output ──
  if ! validate_png "$png"; then
    warn "PNG output appears blank or corrupted (file too small for 4096×4096)"
    warn "Retrying with reduced parameters..."

    # Fallback: scale 1, dpi 150
    local fallback_scale=1
    local fallback_dpi=150
    inject_style "$input" "$png_puml" "$fallback_scale" "$fallback_dpi"
    log "PNG fallback: scale=${fallback_scale}, dpi=${fallback_dpi}"

    curl -sf -X POST -H "Content-Type: text/plain" \
      --data-binary "@${png_puml}" "${PLANTUML_SERVER}/png" -o "$png" || true

    if ! validate_png "$png"; then
      warn "PNG fallback also produced invalid output. PNG may be incomplete."
    fi
  fi

  rm -f "$png_puml"

  # ── Step 5: Report results ──
  local svg_vb png_dim png_size
  svg_vb=$(grep -oE 'viewBox="[^"]*"' "$svg" 2>/dev/null | head -1 || echo "unknown")
  png_dim=$(file "$png" 2>/dev/null | grep -oE '[0-9]+ x [0-9]+' | head -1 || echo "unknown")
  png_size=$(wc -c < "$png" 2>/dev/null | tr -d ' ' || echo "0")

  echo "=== Rendering Complete ==="
  echo "Source: ${puml}"
  echo "SVG:    ${svg} (${svg_vb})"
  echo "PNG:    ${png} (${png_dim}, ${png_size} bytes)"
  echo "Config: SVG=scale${SVG_SCALE}/dpi${SVG_DPI} | PNG=scale${png_scale}/dpi${png_dpi} (target ≤${PNG_MAX}px)"

  # Warn if PNG hit the cap
  if echo "$png_dim" | grep -q "4096"; then
    warn "PNG hit server hard cap (4096). Content may be clipped. Prefer SVG for this diagram."
  fi
}

main "$@"
