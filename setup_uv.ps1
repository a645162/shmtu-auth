# 快速设置 uv 环境的 PowerShell 脚本

Write-Host "正在安装 uv..." -ForegroundColor Green

# 检查是否已安装 uv
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
	Write-Host "uv 未安装，正在安装..." -ForegroundColor Yellow
	# 在 Windows 上安装 uv
	Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    
	Write-Host "uv 安装完成！" -ForegroundColor Green
    
	# 重新加载 PATH
	$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
}
else {
	Write-Host "uv 已安装" -ForegroundColor Green
}

Write-Host "正在初始化项目..." -ForegroundColor Yellow

# 同步依赖
uv sync

Write-Host "设置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法：" -ForegroundColor Cyan
Write-Host "  uv run python start_cli.py         # 运行 CLI 版本" -ForegroundColor White
Write-Host "  uv run python -m shmtu_auth        # 运行模块" -ForegroundColor White
Write-Host "  uv add <package>                   # 添加新依赖" -ForegroundColor White
Write-Host "  uv remove <package>                # 移除依赖" -ForegroundColor White
Write-Host "  uv sync                            # 同步依赖" -ForegroundColor White
Write-Host "  uv run pytest                      # 运行测试" -ForegroundColor White
