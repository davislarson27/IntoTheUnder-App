#!/usr/bin/env bash
set -euo pipefail


###############################################################################

# to run ./compile-to-dmg.sh (optional iconname, not extension)
# run from inside the ITU-App directory itself

# Into The Under — build + (ad-hoc) sign + DMG packaging script
#
# What it does:
#  1) Copies this ITU-App source tree into a signing/work directory
#  2) Runs PyInstaller to produce a .app
#  3) Removes quarantine attributes
#  4) Codesigns the .app (default: ad-hoc sign, like your "codesign --sign -")
#  5) Verifies codesign output
#  6) Creates a DMG (via hdiutil) with an /Applications shortcut inside
#  7) Leaves a copy of the DMG in a specific output location
#
# NOTE:
#  - This script does NOT notarize. It matches your current ad-hoc signing flow.
#  - If you later want Developer ID signing + notarization, I can extend it.
###############################################################################

# ----------------------------
# User-editable configuration
# ----------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ITU-App is the source tree itself (no per-version subfolder anymore).
SOURCE_VERSION_DIR="$SCRIPT_DIR"

# Optional first argument for icon name
if [[ $# -ge 1 ]]; then
  ICON_FILE_NAME="$1"
else
  ICON_FILE_NAME="ITU-Icon"   # default
fi

ICON_REL_PATH="game_files/image_files/${ICON_FILE_NAME}.icns"


# Where to copy/build (your "signingwork" area).
SIGNING_WORK_DIR="${SIGNING_WORK_DIR:-$HOME/signingwork}"

# App display name (PyInstaller --name and .app bundle name)
APP_NAME="${APP_NAME:-Into The Under}"
APP_BUNDLE="${APP_NAME}.app"

# PyInstaller entrypoint script
ENTRYPOINT="${ENTRYPOINT:-itu-mac.py}"

# Data folder inclusion (relative to version folder)
ADD_DATA_SRC_REL="${ADD_DATA_SRC_REL:-game_files}"
ADD_DATA_DEST="${ADD_DATA_DEST:-game_files}"

# Signing identity:
#  - "-" = ad-hoc signature (what you’re doing today)
#  - Or set to something like: "Developer ID Application: Your Name (TEAMID)"
SIGN_IDENTITY="${SIGN_IDENTITY:--}"

# DMG settings
DMG_VOLUME_NAME="${DMG_VOLUME_NAME:-IntoTheUnder}"
DMG_COMPRESSION="${DMG_COMPRESSION:-ULFO}"   # compressed read-only (good default)
DMG_FORMAT="${DMG_FORMAT:-UDZO}"             # UDZO compressed
DMG_SIZE_MB="${DMG_SIZE_MB:-}"               # optional; usually not needed (auto)

# If you want each build in its own subdir, set to 1
CREATE_VERSION_SUBDIR="${CREATE_VERSION_SUBDIR:-1}"

# If 1, delete existing build folders before building (clean run)
CLEAN_OLD="${CLEAN_OLD:-1}"

# ----------------------------
# Derived paths
# ----------------------------

# Version label pulled from game_loop.py's VERSION_NAME (e.g. "intotheunder1.7.0"),
# falling back to the folder name if it can't be found.
VERSION_NAME="$(grep -oE 'VERSION_NAME = "[^"]+"' "$SOURCE_VERSION_DIR/game_loop.py" 2>/dev/null | head -1 | sed -E 's/VERSION_NAME = "(.*)"/\1/')"
VERSION_NAME="${VERSION_NAME:-$(basename "$SOURCE_VERSION_DIR")}"

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"

if [[ "$CREATE_VERSION_SUBDIR" == "1" ]]; then
  BUILD_ROOT="$SIGNING_WORK_DIR/${VERSION_NAME}_${TIMESTAMP}"
else
  BUILD_ROOT="$SIGNING_WORK_DIR/$VERSION_NAME"
fi

PROJECT_DIR="$BUILD_ROOT/$VERSION_NAME"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"
SPEC_GLOB="$PROJECT_DIR"/*.spec

STAGING_DIR="$BUILD_ROOT/dmg_staging"
DMG_TEMP="$BUILD_ROOT/${DMG_VOLUME_NAME}.dmg"

# Keep DMG output in the same place as before: IntoTheUnder/macExports, one
# directory up from ITU-App.
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/../macExports}"
DMG_FINAL="$OUTPUT_DIR/${VERSION_NAME}.dmg"


# ----------------------------
# Helpers
# ----------------------------

die() { echo "❌ $*" >&2; exit 1; }
log() { echo "➡️  $*"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"
}

# ----------------------------
# Preconditions
# ----------------------------

need_cmd python3
need_cmd hdiutil
need_cmd codesign
need_cmd xattr
need_cmd ditto
need_cmd rsync

[[ -d "$SOURCE_VERSION_DIR" ]] || die "SOURCE_VERSION_DIR not found: $SOURCE_VERSION_DIR"
[[ -f "$SOURCE_VERSION_DIR/$ENTRYPOINT" ]] || die "Entry point not found: $SOURCE_VERSION_DIR/$ENTRYPOINT"
[[ -f "$SOURCE_VERSION_DIR/$ICON_REL_PATH" ]] || die "Icon not found: $SOURCE_VERSION_DIR/$ICON_REL_PATH"
[[ -d "$SOURCE_VERSION_DIR/$ADD_DATA_SRC_REL" ]] || die "Data folder not found: $SOURCE_VERSION_DIR/$ADD_DATA_SRC_REL"

mkdir -p "$SIGNING_WORK_DIR"
mkdir -p "$OUTPUT_DIR"

# ----------------------------
# Step 1: Copy source into signing work
# ----------------------------

log "Creating build root: $BUILD_ROOT"
mkdir -p "$BUILD_ROOT"

log "Copying ITU-App source into signing work…"
mkdir -p "$PROJECT_DIR"
# Copy the source tree, excluding VCS/dev cruft that doesn't belong in the build.
rsync -a --delete \
  --exclude '.git' \
  --exclude '.claude' \
  --exclude '__pycache__' \
  --exclude '.DS_Store' \
  --exclude 'testing' \
  "$SOURCE_VERSION_DIR/" "$PROJECT_DIR/"

# ----------------------------
# Step 2: Clean old build artifacts
# ----------------------------

if [[ "$CLEAN_OLD" == "1" ]]; then
  log "Cleaning old PyInstaller artifacts (dist/, build/, *.spec)…"
  rm -rf "$DIST_DIR" "$BUILD_DIR"
  rm -f -- "$PROJECT_DIR"/*.spec 2>/dev/null || true
fi

# ----------------------------
# Step 3: Build .app with PyInstaller
# ----------------------------

log "Building app with PyInstaller…"
cd "$PROJECT_DIR"

# Make sure PyInstaller is available (either globally or in your python env)
command -v pyinstaller >/dev/null 2>&1 || die "PyInstaller not found. Install with: pipx install pyinstaller"

# Note: --add-data syntax is 'SRC:DEST' on macOS
PyInstaller \
  --clean \
  --noconfirm \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICON_REL_PATH" \
  --add-data "${ADD_DATA_SRC_REL}:${ADD_DATA_DEST}" \
  "$ENTRYPOINT"

[[ -d "$DIST_DIR/$APP_BUNDLE" ]] || die "Expected app bundle not found: $DIST_DIR/$APP_BUNDLE"

# ----------------------------
# Step 4: Remove quarantine
# ----------------------------

log "Removing quarantine attributes…"
xattr -dr com.apple.quarantine "$DIST_DIR/$APP_BUNDLE" || true

# ----------------------------
# Step 5: Codesign (ad-hoc by default)
# ----------------------------

log "Signing app bundle (identity: $SIGN_IDENTITY)…"
codesign --force --deep --sign "$SIGN_IDENTITY" "$DIST_DIR/$APP_BUNDLE"

# Optional: set hardened runtime if doing Developer ID (not needed for ad-hoc)
# If you later do Developer ID signing, you likely want:
#   codesign --force --deep --options runtime --timestamp --sign "$SIGN_IDENTITY" ...

log "Verifying signature details…"
codesign -dv --verbose=4 "$DIST_DIR/$APP_BUNDLE" 2>&1 | sed -n '1,80p'

log "Verifying codesign validity…"
codesign --verify --deep --strict --verbose=2 "$DIST_DIR/$APP_BUNDLE"

# ----------------------------
# Step 6: DMG staging folder
# ----------------------------

log "Preparing DMG staging folder…"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

log "Copying app into staging…"
ditto "$DIST_DIR/$APP_BUNDLE" "$STAGING_DIR/$APP_BUNDLE"

log "Adding /Applications shortcut inside DMG…"
ln -s /Applications "$STAGING_DIR/Applications"

cp "$SCRIPT_DIR/LICENCE.md" "$STAGING_DIR/LICENCE.md"
cp "$SCRIPT_DIR/README.md" "$STAGING_DIR/README.md"

# ----------------------------
# Step 7: Create DMG with hdiutil
# ----------------------------

log "Creating DMG…"
rm -f "$DMG_TEMP"

# If you want to force a size, you can pass -size, but auto is usually fine.
# We'll include it only if DMG_SIZE_MB is set.
if [[ -n "${DMG_SIZE_MB}" ]]; then
  hdiutil create \
    -volname "$DMG_VOLUME_NAME" \
    -srcfolder "$STAGING_DIR" \
    -ov \
    -format "$DMG_FORMAT" \
    -size "${DMG_SIZE_MB}m" \
    "$DMG_TEMP"
else
  hdiutil create \
    -volname "$DMG_VOLUME_NAME" \
    -srcfolder "$STAGING_DIR" \
    -ov \
    -format "$DMG_FORMAT" \
    "$DMG_TEMP"
fi

# Optional: additional compression step (usually unnecessary with UDZO)
# hdiutil convert "$DMG_TEMP" -format UDZO -imagekey zlib-level=9 -o "$DMG_TEMP.converted.dmg"

# ----------------------------
# Step 8: Copy DMG to output directory
# ----------------------------

log "Copying DMG to output: $DMG_FINAL"
cp -f "$DMG_TEMP" "$DMG_FINAL"

log "✅ Done!"
echo
echo "Build workspace: $BUILD_ROOT"
echo "App bundle:      $DIST_DIR/$APP_BUNDLE"
echo "DMG output:      $DMG_FINAL"
