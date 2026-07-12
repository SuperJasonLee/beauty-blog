# Install-DailyPublishTask.ps1
# 注册 Windows 定时任务：每天 12:00 执行 daily-publish.ps1
# 需要管理员权限运行

param(
    [switch]$Uninstall
)

$TaskName = "BeautyBlog-DailyPublish"
$TaskDescription = "Beauty-Blog 每日 12:00 自动发布整形文章"
$ScriptPath = Join-Path $PSScriptRoot "daily-publish.ps1"

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "✓ 已卸载定时任务: $TaskName"
    exit 0
}

# 检查脚本是否存在
if (!(Test-Path $ScriptPath)) {
    Write-Error "找不到脚本: $ScriptPath"
    exit 1
}

# 创建触发器: 每天 12:00
$Trigger = New-ScheduledTaskTrigger -Daily -At "12:00"

# 创建操作: 运行 PowerShell 执行脚本
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`"" `
    -WorkingDirectory (Split-Path $ScriptPath)

# 创建设置
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -RestartCount 1 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# 注册任务（当前用户）
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Limited

# 先删除已有任务
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $TaskDescription `
    -Trigger $Trigger `
    -Action $Action `
    -Settings $Settings `
    -Principal $Principal

Write-Host ""
Write-Host "✓ 定时任务已注册: $TaskName"
Write-Host "  触发时间: 每天 12:00"
Write-Host "  脚本路径: $ScriptPath"
Write-Host ""
Write-Host "管理命令:"
Write-Host "  查看: Get-ScheduledTask '$TaskName'"
Write-Host "  暂停: Disable-ScheduledTask '$TaskName'"
Write-Host "  恢复: Enable-ScheduledTask '$TaskName'"
Write-Host "  手动触发: Start-ScheduledTask '$TaskName'"
Write-Host "  卸载: .\install.ps1 -Uninstall"
