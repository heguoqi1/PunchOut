@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================
REM   下班打卡提醒 —— 安装定时任务
REM   需要以管理员身份运行
REM ============================================

set "TASK_NAME=ClockOutReminder"
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%remind.py"

echo.
echo === 下班打卡提醒 —— 安装 ===
echo.

REM 查找 pythonw.exe，找不到则用 python.exe
set "PYTHON_EXE="
for /f "delims=" %%i in ('where pythonw 2^>nul') do (
    if not defined PYTHON_EXE set "PYTHON_EXE=%%i"
)
if not defined PYTHON_EXE (
    for /f "delims=" %%i in ('where python 2^>nul') do (
        if not defined PYTHON_EXE set "PYTHON_EXE=%%i"
    )
)

if not defined PYTHON_EXE (
    echo [错误] 未找到 Python，请先安装 Python 并加入 PATH
    pause
    exit /b 1
)

echo Python:     %PYTHON_EXE%
echo 脚本路径:    %SCRIPT_PATH%
echo 任务名:      %TASK_NAME%
echo 触发时间:    每天 18:01
echo.

REM 删除已存在的同名任务（幂等）
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

REM 创建定时任务
schtasks /Create ^
    /TN "%TASK_NAME%" ^
    /TR "\"%PYTHON_EXE%\" \"%SCRIPT_PATH%\"" ^
    /SC DAILY ^
    /ST 18:01 ^
    /RL HIGHEST ^
    /F

if !ERRORLEVEL! EQU 0 (
    echo.
    echo [成功] 定时任务已创建
    echo.
    echo 测试方法：
    echo   1. 打开「任务计划程序」
    echo   2. 找到任务 "%TASK_NAME%"
    echo   3. 右键 → 运行
    echo.
    echo 卸载方法：双击 uninstall.bat
) else (
    echo.
    echo [失败] 请以管理员身份运行此脚本
)

echo.
pause
