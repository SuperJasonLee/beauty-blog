#!/usr/bin/env bash
# install.sh —— 一键安装 launchd 调度（macOS）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_SRC="$SCRIPT_DIR/com.beautyblog.dailypublish.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.beautyblog.dailypublish.plist"

# 0. 健全性检查
if [ ! -f "$PLIST_SRC" ]; then
  echo "ERROR: plist not found at $PLIST_SRC"
  exit 1
fi

# 1. 复制 plist 到 ~/Library/LaunchAgents/
mkdir -p "$HOME/Library/LaunchAgents"
cp "$PLIST_SRC" "$PLIST_DEST"
echo "✓ Plist installed: $PLIST_DEST"

# 2. 如果已加载，先卸载（幂等）
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# 3. 加载
if launchctl load "$PLIST_DEST" 2>&1; then
  echo "✓ LaunchAgent loaded."
else
  echo "✗ launchctl load failed."
  exit 1
fi

# 4. 显示状态
echo ""
echo "Current status:"
launchctl list | grep beautyblog || echo "  (not visible in launchctl list — may be a label mismatch)"

# 5. 提示下一步
echo ""
echo "Installed. The pipeline will run daily at 12:00 (local time)."
echo ""
echo "Useful commands:"
echo "  Trigger now (test):    ./scripts/daily-publish/daily-publish.sh"
echo "  View logs:             tail -f logs/daily-publish/\$(ls -t logs/daily-publish/ | head -1)"
echo "  Pause (kill switch):   touch scripts/daily-publish/.disabled"
echo "  Resume:                rm scripts/daily-publish/.disabled"
echo "  Uninstall:             ./scripts/daily-publish/uninstall.sh"
echo "  List loaded agents:    launchctl list | grep beautyblog"
