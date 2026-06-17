# SHMTU Auth Headless - Docker 管理脚本 (Windows)

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "build", "help")]
    [string]$Command = "help"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ComposeFile = Join-Path $ScriptDir "docker-compose.yml"

function Show-Usage {
    Write-Host "用法: .\start.ps1 <命令>"
    Write-Host ""
    Write-Host "命令:"
    Write-Host "  start     启动服务"
    Write-Host "  stop      停止服务"
    Write-Host "  restart   重启服务"
    Write-Host "  status    查看状态"
    Write-Host "  logs      查看日志"
    Write-Host "  build     构建镜像"
    Write-Host "  help      显示帮助"
}

function Start-Service {
    Write-Host "[INFO] 启动 shmtu-auth-headless..." -ForegroundColor Green
    docker compose -f $ComposeFile up -d
    Write-Host "[INFO] 服务已启动" -ForegroundColor Green
    Show-Status
}

function Stop-Service {
    Write-Host "[INFO] 停止 shmtu-auth-headless..." -ForegroundColor Green
    docker compose -f $ComposeFile down
    Write-Host "[INFO] 服务已停止" -ForegroundColor Green
}

function Restart-Service {
    Write-Host "[INFO] 重启 shmtu-auth-headless..." -ForegroundColor Green
    docker compose -f $ComposeFile restart
    Write-Host "[INFO] 服务已重启" -ForegroundColor Green
}

function Show-Status {
    docker compose -f $ComposeFile ps
}

function Show-Logs {
    docker compose -f $ComposeFile logs -f --tail=100
}

function Build-Image {
    Write-Host "[INFO] 构建镜像..." -ForegroundColor Green
    docker compose -f $ComposeFile build --no-cache
    Write-Host "[INFO] 构建完成" -ForegroundColor Green
}

# 主逻辑
switch ($Command) {
    "start"   { Start-Service }
    "stop"    { Stop-Service }
    "restart" { Restart-Service }
    "status"  { Show-Status }
    "logs"    { Show-Logs }
    "build"   { Build-Image }
    "help"    { Show-Usage }
}
