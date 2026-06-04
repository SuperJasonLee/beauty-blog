#!/usr/bin/env bash
# daily-publish.sh
# ----------------------------------------------------------------
# Daily automated publish pipeline.
# 每天 12:00 由 launchd 触发：5 阶段全自动（无需 review）。
#
# Stages:
#   1-4: 跑 scripts/crawl-eye-surgery-news/ pipeline
#        (crawl → image download → post generation)
#   5:   翻转 draft: true → draft: false（即时发布）
#   6:   git auto-commit (optional push)
#   7:   macOS notification
#
# Kill switch: 在同目录创建 .disabled 文件可暂停
# Config:      复制 .env.example 为 .env 后按需修改
# ----------------------------------------------------------------
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs/daily-publish"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y%m%d_%H%M%S).log"

# 加载可选配置
[ -f "$SCRIPT_DIR/.env" ] && source "$SCRIPT_DIR/.env"

log()  { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }
notify() {
  local msg="$1"
  local sound="${2:-default}"
  osascript -e "display notification \"$msg\" with title \"Beauty-Blog 12:00\" sound name \"$sound\"" \
    2>/dev/null || echo "(notification failed)"
}

log "=========================================="
log "Daily publish pipeline started"
log "PID=$$ HOST=$(hostname) User=$(whoami)"
log "=========================================="

# ---------- Kill switch ----------
if [ -f "$SCRIPT_DIR/.disabled" ]; then
  log "Kill switch active (.disabled file present). Skipping."
  notify "Daily publish skipped (kill switch)."
  exit 0
fi

cd "$PROJECT_ROOT" || { log "FATAL: cannot cd to $PROJECT_ROOT"; exit 1; }

# ---------- Stage 1-4: 跑现有 pipeline ----------
log "Stage 1-4: Running crawl:eye-news..."
PIPELINE_START=$(date +%s)
if npm run crawl:eye-news >> "$LOG" 2>&1; then
  PIPELINE_ELAPSED=$(( $(date +%s) - PIPELINE_START ))
  log "Pipeline OK in ${PIPELINE_ELAPSED}s."
else
  PIPELINE_ELAPSED=$(( $(date +%s) - PIPELINE_START ))
  log "ERROR: Pipeline failed in ${PIPELINE_ELAPSED}s. See $LOG for details."
  notify "Pipeline FAILED. See $LOG" "Basso"
  exit 1
fi

# ---------- Stage 5: 翻转 draft: true → draft: false ----------
log "Stage 5: Publishing drafts (draft: true → false)..."
PUBLISHED=0
PUBLISHED_FILES=()
for f in content/zh-cn/posts/eye-surgery-news/*.md content/en/posts/eye-surgery-news/*.md; do
  [ -f "$f" ] || continue
  if grep -q "^draft: true" "$f" 2>/dev/null; then
    # 备份原文件到 .bak（如果已有 .bak 则覆盖）
    cp "$f" "$f.bak"
    sed -i '' "s/^draft: true/draft: false/" "$f"
    PUBLISHED=$((PUBLISHED + 1))
    PUBLISHED_FILES+=("$f")
    log "  ✓ $f"
  fi
done

# 同时更新 pipeline 生成的、可能位于其他位置的 draft（保险起见全仓扫描）
EXTRA=$(grep -rl "^draft: true" content/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$EXTRA" -gt 0 ]; then
  log "Found $EXTRA other drafts; leaving them untouched (manual review path)."
fi

log "Stage 5 done: $PUBLISHED posts published."

# ---------- Stage 6: Git auto-commit ----------
if [ "${AUTO_COMMIT:-true}" = "true" ]; then
  log "Git: staging changes..."
  # 收 pipeline 产物 + 今天的图片
  git add content/ static/images/ 2>&1 | tee -a "$LOG" || true

  if [ -n "$(git status --porcelain content/ static/images/ 2>/dev/null)" ]; then
    COMMIT_MSG="auto-publish: $(date +%Y-%m-%d) daily post

Triggered by: launchd com.beautyblog.dailypublish
Posts published: $PUBLISHED
Log: $LOG"
    if git commit -m "$COMMIT_MSG" >> "$LOG" 2>&1; then
      log "Committed: $(git log -1 --pretty=%h)"

      # 可选 push
      if [ "${AUTO_PUSH:-false}" = "true" ]; then
        if git push >> "$LOG" 2>&1; then
          log "Pushed to remote."
        else
          log "Push failed (non-fatal). Commit is local only."
        fi
      else
        log "AUTO_PUSH=false; commit is local. Run 'git push' manually if needed."
      fi
    else
      log "Commit failed (non-fatal)."
    fi
  else
    log "No content changes to commit."
  fi
fi

# ---------- Stage 7: 通知 ----------
log "=========================================="
log "Done. $PUBLISHED posts published."
[ "$PUBLISHED" -gt 0 ] && log "Files: ${PUBLISHED_FILES[*]}"
log "Log: $LOG"
log "=========================================="

if [ "$PUBLISHED" -gt 0 ]; then
  notify "Published $PUBLISHED post(s). See $LOG"
else
  notify "Pipeline ran but no new drafts. See $LOG"
fi

exit 0
