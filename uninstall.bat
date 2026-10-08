@echo off
chcp 65001 >nul
setlocal

set "TASK_NAME=ClockOutReminder"

echo.
echo === 下班打卡提醒 —— 卸载 ===
echo.

schtasks /Delete /TN "%TASK_NAME%" /F

if %ERRORLEVEL% EQU 0 (
    echo [成功] 任务 "%TASK_NAME%" 已删除
) else (
    echo [提示] 任务不存在或删除失败
)

echo.
pause
