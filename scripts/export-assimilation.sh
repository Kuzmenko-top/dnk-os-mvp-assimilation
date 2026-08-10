#!/bin/bash
set -e

# Configuration
EXPORT_DIR="/tmp/dnk-assimilation-export"
REPO_URL="https://github.com/Kuzmenko-top/dnk-os-mvp-assimilation.git"

# Clean previous export
rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR"

# Copy artifacts (adjust paths as needed)
mkdir -p "$EXPORT_DIR/DNKOS_MVP"
cp -r DNKOS_MVP/docs "$EXPORT_DIR/DNKOS_MVP/"
cp -r DNKOS_MVP/skills "$EXPORT_DIR/DNKOS_MVP/"

# Make sure SEC specs are in specs directory in EXPORT_DIR
cp "$EXPORT_DIR/DNKOS_MVP/docs/tech/standards/DNK-SEC-001_canvas-sandbox.md" "$EXPORT_DIR/DNKOS_MVP/docs/tech/specs/"
cp "$EXPORT_DIR/DNKOS_MVP/docs/tech/standards/DNK-SEC-002_sandbox-network-egress.md" "$EXPORT_DIR/DNKOS_MVP/docs/tech/specs/"

# Navigate to export directory
cd "$EXPORT_DIR"

# Initialize git if not already
if [ ! -d ".git" ]; then
  git init
  git remote add origin "$REPO_URL" || true
  git checkout -b main 2>/dev/null || git checkout main
fi

# Stage and commit
git add .
git diff --cached --quiet || git commit -m "Export assimilation artifacts $(date '+%Y-%m-%d %H:%M')"

# Push
git push -u origin main

echo "✅ Export complete. Artifacts pushed to $REPO_URL"
