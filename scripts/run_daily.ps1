# DailyResearch - Windows PowerShell 启动脚本
# 用法:
#   .\run_daily.ps1             生成提示词
#   .\run_daily.ps1 -Validate   验证配置
#   .\run_daily.ps1 -Stats      查看报告统计
#   .\run_daily.ps1 -Queries    输出搜索查询

param(
    [switch]$Validate,
    [switch]$Stats,
    [switch]$Queries
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Set-Location $ProjectDir

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  DailyResearch - 每日科研热点追踪" -ForegroundColor Yellow
Write-Host "  日期: $(Get-Date -Format 'yyyy-MM-dd')" -ForegroundColor Cyan
Write-Host "  平台: Windows" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Check API key
if (-not $env:ANTHROPIC_API_KEY) {
    Write-Host "[WARN] ANTHROPIC_API_KEY not set" -ForegroundColor Yellow
    Write-Host "  Set with: `$env:ANTHROPIC_API_KEY='your_key'" -ForegroundColor Gray
}

# Run command
if ($Validate) {
    Write-Host "`nValidating configuration..." -ForegroundColor Cyan
    python scripts/research_agent.py validate
} elseif ($Stats) {
    python scripts/research_agent.py stats
} elseif ($Queries) {
    python scripts/research_agent.py queries
} else {
    Write-Host "`nGenerating research prompt..." -ForegroundColor Cyan
    Write-Host ""
    python scripts/research_agent.py prompt
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  In Claude Code, follow CLAUDE.md workflow:" -ForegroundColor Yellow
    Write-Host "  1. Use WebSearch for each domain" -ForegroundColor White
    Write-Host "  2. Use WebFetch for paper details" -ForegroundColor White
    Write-Host "  3. Save report to output/ directory" -ForegroundColor White
    Write-Host "============================================" -ForegroundColor Cyan
}
