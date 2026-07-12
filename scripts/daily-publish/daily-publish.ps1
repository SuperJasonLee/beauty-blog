# Daily Publish - Windows PowerShell Script
# 每日自动发布整形文章 (Windows Task Scheduler 版)
# 用法: 由 Windows Task Scheduler 每天 12:00 调用

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$LogDir = Join-Path $ProjectRoot "logs\daily-publish"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "$Timestamp.log"

# 创建日志目录
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

function Notify($msg) {
    # Windows toast notification (burnttoast module if available, otherwise fallback)
    try {
        if (Get-Module -ListAvailable -Name BurntToast) {
            New-BurntToastNotification -Text "Beauty-Blog Daily", $msg -AppLogo "$ProjectRoot\static\favicon.ico"
        } else {
            Log "Notification: $msg"
        }
    } catch {
        Log "Notification failed (non-fatal): $_"
    }
}

Log "=========================================="
Log "Daily publish pipeline started"
Log "PID=$PID Host=$env:COMPUTERNAME User=$env:USERNAME"
Log "=========================================="

# ---------- Kill switch ----------
$DisabledFile = Join-Path $PSScriptRoot ".disabled"
if (Test-Path $DisabledFile) {
    Log "Kill switch active (.disabled file present). Skipping."
    Notify "Daily publish skipped (kill switch)."
    exit 0
}

# ---------- Stage 1-4: Run pipeline ----------
Log "Stage 1-4: Running crawl:eye-news..."
$PipelineStart = Get-Date

try {
    Push-Location (Join-Path $ProjectRoot "scripts\crawl-eye-surgery-news")
    & python run.py 2>&1 | Tee-Object -Append -FilePath $LogFile
    if ($LASTEXITCODE -ne 0) { throw "Pipeline exited with code $LASTEXITCODE" }
    $PipelineElapsed = ((Get-Date) - $PipelineStart).TotalSeconds
    Log "Pipeline OK in ${PipelineElapsed}s."
} catch {
    $PipelineElapsed = ((Get-Date) - $PipelineStart).TotalSeconds
    Log "ERROR: Pipeline failed in ${PipelineElapsed}s. See $LogFile"
    Notify "Pipeline FAILED. See $LogFile"
    exit 1
} finally {
    Pop-Location
}

# ---------- Stage 5: 翻转 draft: true → draft: false ----------
Log "Stage 5: Publishing drafts (draft: true → false)..."
$Published = 0
$PublishedFiles = @()

$draftFiles = Get-ChildItem -Path "$ProjectRoot\content\zh-cn\posts" -Filter "*.md" -Recurse
$draftFiles += Get-ChildItem -Path "$ProjectRoot\content\en\posts" -Filter "*.md" -Recurse

foreach ($f in $draftFiles) {
    $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    if ($content -match "^draft: true") {
        # 备份
        Copy-Item $f.FullName "$($f.FullName).bak" -Force
        # 替换
        $newContent = $content -replace "^draft: true", "draft: false"
        [System.IO.File]::WriteAllText($f.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
        $Published++
        $PublishedFiles += $f.Name
        Log "  ✓ $($f.Name)"
    }
}

Log "Stage 5 done: $Published posts published."

# ---------- Stage 6: Git auto-commit ----------
$AutoCommit = if ($env:AUTO_COMMIT) { $env:AUTO_COMMIT } else { "true" }

if ($AutoCommit -eq "true") {
    Log "Git: staging changes..."
    Push-Location $ProjectRoot
    try {
        & git add content/ static/images/ 2>&1 | Out-Null

        $status = & git status --porcelain content/ static/images/
        if ($status) {
            $CommitMsg = "auto-publish: $(Get-Date -Format 'yyyy-MM-dd') daily post`n`nTriggered by: Windows Task Scheduler`nPosts published: $Published`nLog: $LogFile"
            & git commit -m $CommitMsg 2>&1 | Tee-Object -Append -FilePath $LogFile
            Log "Committed: $(git log -1 --pretty=%h)"

            $AutoPush = if ($env:AUTO_PUSH) { $env:AUTO_PUSH } else { "false" }
            if ($AutoPush -eq "true") {
                & git push 2>&1 | Tee-Object -Append -FilePath $LogFile
                Log "Pushed to remote."
            } else {
                Log "AUTO_PUSH=false; commit is local. Run 'git push' manually."
            }
        } else {
            Log "No content changes to commit."
        }
    } catch {
        Log "Git commit failed (non-fatal): $_"
    } finally {
        Pop-Location
    }
}

# ---------- Stage 7: 通知 ----------
Log "=========================================="
Log "Done. $Published posts published."
if ($Published -gt 0) { Log "Files: $($PublishedFiles -join ', ')" }
Log "Log: $LogFile"
Log "=========================================="

if ($Published -gt 0) {
    Notify "Published $Published post(s). See $LogFile"
} else {
    Notify "Pipeline ran but no new drafts. See $LogFile"
}
