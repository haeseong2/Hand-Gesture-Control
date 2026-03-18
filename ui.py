import threading
import tkinter as tk
from camera_loop import run_camera

"""
[start_camera]
카메라 스레드를 실행하는 함수
이미 실행 중이면 중복 실행을 막고, 별도 스레드에서 카메라 루프 실행

on_close
UI 종료 시 호출되는 함수
카메라 루프를 종료하고 프로그램 전체 종료

start_ui
사용자가 제스처를 설정할 수 있는 UI 생성 함수
볼륨 UP/DOWN, LOCK 손, LOCK 유지 시간 설정 가능

gesture_config
제스처 설정 값을 저장하는 딕셔너리
volume_up / volume_down : 볼륨 제어에 사용할 손
lock_hand              : LOCK 기능에 사용할 손
lock_delay             : LOCK 발동까지 필요한 시간

camera_thread
카메라 실행용 백그라운드 스레드

stop_event
카메라 루프 종료를 위한 이벤트 객체
"""

camera_thread = None
stop_event = threading.Event()


gesture_config = {
    "volume_up": "Right",
    "volume_down": "Left",
    "lock_hand": "Right",
    "lock_delay": 5
}


options = {
    "✊ Right": "Right",
    "✊ Left": "Left"
}

lock_options = {
    "✋ Right": "Right",
    "✋ Left": "Left"
}

time_options = ["3", "5", "7", "10"]


def start_camera():

    global camera_thread, stop_event

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

    global stop_event

    stop_event.set()
    root.destroy()


def start_ui():

    global root

    root = tk.Tk()
    root.title("Gesture Controller")
    root.geometry("320x320")

    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Button(root,
        text="Start Camera",
        command=start_camera,
        width=20,
        height=2).pack(pady=10)

    tk.Label(root, text="Volume UP Gesture").pack()
    up_var = tk.StringVar(value="✊ Right")

    tk.OptionMenu(root, up_var, *options.keys(),
        command=lambda x: gesture_config.update({"volume_up": options[x]})
    ).pack()

    tk.Label(root, text="Volume DOWN Gesture").pack()
    down_var = tk.StringVar(value="✊ Left")

    tk.OptionMenu(root, down_var, *options.keys(),
        command=lambda x: gesture_config.update({"volume_down": options[x]})
    ).pack()

    tk.Label(root, text="Lock Gesture (Open Hand)").pack()
    lock_var = tk.StringVar(value="✋ Right")

    tk.OptionMenu(root, lock_var, *lock_options.keys(),
        command=lambda x: gesture_config.update({"lock_hand": lock_options[x]})
    ).pack()

    tk.Label(root, text="Lock Hold Time (sec)").pack()
    time_var = tk.StringVar(value="5")

    tk.OptionMenu(root, time_var, *time_options,
        command=lambda x: gesture_config.update({"lock_delay": int(x)})
    ).pack()

    root.mainloop()