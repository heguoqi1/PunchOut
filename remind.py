# -*- coding: utf-8 -*-
"""
下班打卡提醒弹窗
由 Windows 任务计划程序在每天 18:01 触发启动
"""
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

WINDOW_TITLE = "⏰ 下班打卡提醒"
WINDOW_MESSAGE = "该打卡啦！别忘了哦"
SNOOZE_MINUTES = 5
SCRIPT_PATH = os.path.abspath(__file__)


def get_python_exe():
    """优先返回 pythonw.exe，避免弹控制台窗口"""
    exe = sys.executable
    pythonw = exe.replace("python.exe", "pythonw.exe")
    return pythonw if os.path.exists(pythonw) else exe


def schedule_snooze(root):
    """关闭当前窗口，SNOOZE_MINUTES 分钟后再次弹窗"""
    python_exe = get_python_exe()
    # 用 timeout 延时 N 秒后，启动一个新的本进程
    delay = SNOOZE_MINUTES * 60
    cmd = (
        f'timeout /t {delay} /nobreak >nul & '
        f'"{python_exe}" "{SCRIPT_PATH}"'
    )
    subprocess.Popen(cmd, shell=True)
    root.destroy()


def build_window():
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    width, height = 360, 180
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    # 置顶 + 抢焦点
    root.attributes("-topmost", True)
    root.lift()
    root.focus_force()
    # 200ms 后再次置顶，防止被其他窗口盖住
    root.after(200, lambda: root.attributes("-topmost", True))

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        frame, text=WINDOW_TITLE,
        font=("Microsoft YaHei", 14, "bold"),
    ).pack(pady=(0, 10))

    ttk.Label(
        frame, text=WINDOW_MESSAGE,
        font=("Microsoft YaHei", 11),
    ).pack(pady=(0, 20))

    btn_frame = ttk.Frame(frame)
    btn_frame.pack()

    ttk.Button(
        btn_frame, text="已打卡 ✓",
        command=root.destroy, width=15,
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        btn_frame, text=f"{SNOOZE_MINUTES} 分钟后再提醒",
        command=lambda: schedule_snooze(root), width=15,
    ).pack(side=tk.LEFT, padx=5)

    return root


def main():
    root = build_window()
    root.mainloop()


if __name__ == "__main__":
    main()
