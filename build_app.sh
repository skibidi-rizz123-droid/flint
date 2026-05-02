#!/bin/bash
# ─────────────────────────────────────────────
#  build_app.sh  —  builds Flint.app + Flint.dmg
#  Run this any time you update lang.py.
#  Email Flint.dmg to friends — that's it.
# ─────────────────────────────────────────────

APP="Flint.app"
DMG="Flint.dmg"
DIR="$(cd "$(dirname "$0")" && pwd)"
STAGING="/tmp/flint-dmg-staging"

# ── Find python3 path at build time so .app works without shell PATH ──
PYTHON3_PATH="$(which python3)"
if [ -z "$PYTHON3_PATH" ]; then
    PYTHON3_PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
fi
echo "Using python3 at: $PYTHON3_PATH"

# Needed so the macOS menu bar says "Flint" instead of "Python" (Tk quirk).
echo "Ensuring PyObjC for correct menu-bar name..."
"$PYTHON3_PATH" -m pip install -q "pyobjc-framework-Cocoa>=10" 2>/dev/null \
    || echo "  ⚠  pip install pyobjc-framework-Cocoa failed — install it manually if the menu still says Python"

echo "Building icon..."
"$PYTHON3_PATH" "$DIR/make_icon.py"

echo "Building $APP..."

# ── Clean ─────────────────────────────────────
rm -rf "$DIR/$APP"
rm -rf "$STAGING"
rm -f  "$DIR/$DMG"

# ── Bundle structure ──────────────────────────
mkdir -p "$DIR/$APP/Contents/MacOS"
mkdir -p "$DIR/$APP/Contents/Resources"

cp "$DIR/lang.py"    "$DIR/$APP/Contents/Resources/lang.py"
cp "$DIR/Flint.icns" "$DIR/$APP/Contents/Resources/Flint.icns"

# ── Launcher (hardcode python3 path so macOS .app gets the right interpreter) ──
LAUNCHER_PATH="$DIR/$APP/Contents/MacOS/Flint"
cat > "$LAUNCHER_PATH" << ENDOFSCRIPT
#!/bin/bash
FLINT_HOME="\$HOME/.flint"
BUNDLED="\$(cd "\$(dirname "\$0")/../Resources" && pwd)/lang.py"

if [ ! -f "\$FLINT_HOME/lang.py" ]; then
    mkdir -p "\$FLINT_HOME"
    cp "\$BUNDLED" "\$FLINT_HOME/lang.py"
fi

mkdir -p "\$HOME/Documents/flint"

# Keep Flint launcher as the app process so macOS shows Flint icon/name.
"${PYTHON3_PATH}" "\$FLINT_HOME/lang.py" &
FLINT_CHILD_PID=\$!
wait \$FLINT_CHILD_PID
exit \$?
ENDOFSCRIPT
chmod +x "$LAUNCHER_PATH"

echo "  Launcher python: $(grep 'exec ' "$LAUNCHER_PATH")"

# ── Info.plist ────────────────────────────────
cat > "$DIR/$APP/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>           <string>Flint</string>
    <key>CFBundleDisplayName</key>    <string>Flint</string>
    <key>CFBundleIdentifier</key>     <string>com.henrymarcais.flint</string>
    <key>CFBundleVersion</key>        <string>0.1</string>
    <key>CFBundleShortVersionString</key> <string>0.1</string>
    <key>CFBundleExecutable</key>     <string>Flint</string>
    <key>CFBundleIconFile</key>       <string>Flint</string>
    <key>CFBundlePackageType</key>    <string>APPL</string>
    <key>LSMinimumSystemVersion</key> <string>11.0</string>
    <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

echo "  ✓  Built Flint.app"

# ── DMG staging area ──────────────────────────
echo "Building $DMG..."

mkdir -p "$STAGING"
cp -r "$DIR/$APP" "$STAGING/"
ln -s /Applications "$STAGING/Applications"

# ── Create DMG directly ───────────────────────
hdiutil create \
    -volname "Install Flint" \
    -srcfolder "$STAGING" \
    -ov -format UDZO \
    "$DIR/$DMG" > /dev/null

rm -rf "$STAGING"

echo "  ✓  Built Flint.dmg"
echo ""
echo "  ┌─────────────────────────────────────────┐"
echo "  │  Email Flint.dmg to anyone with a Mac.  │"
echo "  │  They open it → drag Flint to Apps →    │"
echo "  │  Done. Auto-updates happen on launch.   │"
echo "  └─────────────────────────────────────────┘"
echo ""
echo "  To publish an update to everyone:"
echo "  ./push_update.sh"
