"""
[run_camera]
카메라 루프 실행 + 제스처 처리 + UI 출력
"""

import cv2
import time
from core.camera import get_camera
from core.hand_detector import HandDetector
from core.volume_controller import VolumeController
from utils.draw_overlay import draw_ui
from gesture.gesture_manager import GestureManager


def run_camera(stop_event, gesture_config):
    cap = get_camera()
    if cap is None or not cap.isOpened():
        print("Camera open failed")
        return

    detector = HandDetector()
    volume = VolumeController()
    gesture_manager = GestureManager(gesture_config)

    pTime = 0

    cv2.namedWindow("Gesture Control")

    while not stop_event.is_set():

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        hand_data = detector.detect(frame)

        if hand_data:
            detector.draw(frame, hand_data)

        result = gesture_manager.process(hand_data)

        # 디버깅
        # print(result)

        mode = result.get("mode", "")
        countdown = result.get("countdown", 0)
        lock_mode = result.get("lock_mode", False)

        vol = gesture_manager.volume.volPercent

        # 볼륨 적용
        volume.set_volume(vol)

        # FPS
        cTime = time.time()
        fps = 1 / max((cTime - pTime), 0.001)
        pTime = cTime

        draw_ui(frame, mode, vol, fps, lock_mode, countdown)
        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) == 27:
            break

        try:
            if cv2.getWindowProperty("Gesture Control", cv2.WND_PROP_VISIBLE) < 1:
                break
        except:
            break

    cap.release()
    cv2.destroyAllWindows()