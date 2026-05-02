#!/bin/bash
# ─────────────────────────────────────────────
#  push_update.sh
#  Run this whenever you want to push an update
#  to all Flint users worldwide.
#
#  SETUP (one time only):
#  1. Create a GitHub account at github.com
#  2. Create a new repo called "flint"
#  3. Run:  git init && git remote add origin https://github.com/YOUR_USERNAME/flint.git
#  4. Set GITHUB_REPO = "YOUR_USERNAME/flint" inside lang.py
# ─────────────────────────────────────────────

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# ── Bump the patch version in lang.py ────────
CURRENT=$(grep '^VERSION' lang.py | head -1 | cut -d'"' -f2)
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

sed -i '' "s/^VERSION     = \"$CURRENT\"/VERSION     = \"$NEW_VERSION\"/" lang.py

echo "  Version: $CURRENT → $NEW_VERSION"

# ── Commit and push ───────────────────────────
git add lang.py
git commit -m "Flint $NEW_VERSION"
git push

echo ""
echo "  ✓  Update pushed!"
echo "  All users will receive v$NEW_VERSION automatically on next launch."
