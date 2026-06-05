@echo off
REM DailyResearch - Windows 科研热点追踪启动脚本
REM 用法: 双击运行，或在任务计划程序中调度

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

cd /d "%PROJECT_DIR%"

echo ============================================
echo   DailyResearch - 每日科研热点追踪
echo   日期: %date%
echo ============================================
echo.

REM 检查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请确保 Python 已安装并加入 PATH
    pause
    exit /b 1
)

REM 检查 API 密钥
if "%ANTHROPIC_API_KEY%"=="" (
    echo [警告] ANTHROPIC_API_KEY 环境变量未设置
    echo   请运行: set ANTHROPIC_API_KEY=your_key_here
    echo.
)

REM 生成研究提示词
echo [1/2] 生成搜索提示词...
python scripts\research_agent.py prompt
echo.
echo [2/2] 提示词已生成。
echo.
echo ============================================
echo   请在 Claude Code 中执行以下操作：
echo   1. 阅读上方输出提示词
echo   2. 按照 CLAUDE.md 定义的流程搜索
echo   3. 保存报告到 output\ 目录
echo ============================================
echo.
pause
