"""
[start_ui]
UI 실행 함수

[start_camera]
카메라 스레드 실행

[on_close]
UI 종료 시 전체 프로그램 종료

gesture_config : 제스처 설정 저장
"""

import threading
import tkinter as tk
from camera_loop import run_camera

camera_thread = None
stop_event = threading.Event()

gesture_config = {
    "volume_up": "right",
    "volume_down": "left",
    "lock_hand": "right",
    "lock_delay": 5
}

options = {
    "✊ Right": "right",
    "✊ Left": "left"
}

lock_options = {
    "✋ Right": "right",
    "✋ Left": "left"
}

time_options = ["3", "5", "7", "10"]


def start_camera():
    global camera_thread

    if camera_thread and camera_thread.is_alive():
        return

    stop_event.clear()

    camera_thread = threading.Thread(
        target=run_camera,
        args=(stop_event, gesture_config),
        daemon=True
    )
    camera_thread.start()


def on_close():
    stop_event.set()
    root.destroy()


def start_ui():
    global root

    root = tk.Tk()
    root.title("Gesture Controller")
    root.geometry("320x320")

    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Button(root, text="Start Camera",
              command=start_camera, width=20, height=2).pack(pady=10)

    tk.Label(root, text="Volume UP").pack()
    up_var = tk.StringVar(value="✊ Right")
    tk.OptionMenu(root, up_var, *options.keys(),
        command=lambda x: gesture_config.update({"volume_up": options[x]})
    ).pack()

    tk.Label(root, text="Volume DOWN").pack()
    down_var = tk.StringVar(value="✊ Left")
    tk.OptionMenu(root, down_var, *options.keys(),
        command=lambda x: gesture_config.update({"volume_down": options[x]})
    ).pack()

    tk.Label(root, text="Lock Hand").pack()
    lock_var = tk.StringVar(value="✋ Right")
    tk.OptionMenu(root, lock_var, *lock_options.keys(),
        command=lambda x: gesture_config.update({"lock_hand": lock_options[x]})
    ).pack()

    tk.Label(root, text="Lock Time").pack()
    time_var = tk.StringVar(value="5")
    tk.OptionMenu(root, time_var, *time_options,
        command=lambda x: gesture_config.update({"lock_delay": int(x)})
    ).pack()

    root.mainloop()