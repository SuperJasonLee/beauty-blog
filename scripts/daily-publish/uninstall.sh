#!/usr/bin/env bash
# uninstall.sh —— 卸载 launchd 调度
set -euo pipefail

PLIST="$HOME/Library/LaunchAgents/com.beautyblog.dailypublish.plist"

if [ -f "$PLIST" ]; then
  launchctl unload "$PLIST" 2>/dev/null && echo "✓ Unloaded from launchd." || echo "  (was not loaded)"
  rm "$PLIST"
  echo "✓ Removed $PLIST"
  echo ""
  echo "Daily publish disabled. Reinstall with: ./scripts/daily-publish/install.sh"
else
  echo "Not installed (plist not found at $PLIST)."
fi
