"""
[distance]
두 랜드마크 좌표 사이의 거리를 계산하는 함수
손가락이 펴졌는지/접혔는지 판단하는 기준으로 사용

p1, p2 : Mediapipe landmark 객체 (x, y 좌표 포함)
[run_camera]
카메라를 실행하고 제스처를 인식하여 볼륨 및 LOCK 기능을 제어하는 메인 루프

stop_event        : UI 종료 시 루프 종료를 위한 이벤트 객체
gesture_config    : 제스처 설정 값 (손 종류, LOCK 시간 등)

volPercent        : 현재 볼륨 값 (0~100)
lastChange        : 마지막 볼륨 변경 시각 (중복 입력 방지)
changeDelay       : 입력 딜레이 시간 (연속 입력 방지)

pTime             : 이전 프레임 시간 (FPS 계산용)

last_mode         : 마지막 동작 상태 저장 (UI 유지용)
mode_timer        : 마지막 상태 변경 시간
mode_duration     : 상태 표시 유지 시간

lock_mode         : LOCK 상태 여부
palm_start_time   : 손바닥 펼친 시작 시간
countdown         : LOCK까지 남은 시간 표시

lock_delay        : LOCK 활성화까지 필요한 유지 시간
lock_hand         : LOCK에 사용할 손 (Right / Left)
"""

import cv2
import time
import math
from camera import get_camera
from hand_detector import HandDetector
from volume_controller import VolumeController
from draw_overlay import draw_ui


def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def run_camera(stop_event, gesture_config):

    cap = get_camera()
    if cap is None or not cap.isOpened():
        print("Camera open failed")
        return

    detector = HandDetector()
    volume = VolumeController()

    volPercent = 80
    lastChange = 0
    changeDelay = 0.15

    pTime = 0

    last_mode = ""
    mode_timer = 0
    mode_duration = 0.7

    lock_mode = False
    palm_start_time = None
    countdown = 0

    cv2.namedWindow("Gesture Control")

    while not stop_event.is_set():

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = detector.detect(frame)

        mode = ""

        if results and results.multi_hand_landmarks:

            for idx, handLms in enumerate(results.multi_hand_landmarks):

                lm = handLms.landmark
                handedness = results.multi_handedness[idx].classification[0].label
                palm = lm[9]

                # 손가락 거리 계산
                d1 = distance(lm[8], palm)
                d2 = distance(lm[12], palm)
                d3 = distance(lm[16], palm)
                d4 = distance(lm[20], palm)

                # 주먹 / 펼침 판단
                fist = (d1 < 0.1 and d2 < 0.1 and d3 < 0.1 and d4 < 0.1)
                open_hand = (d1 > 0.2 and d2 > 0.2 and d3 > 0.2 and d4 > 0.2)

                lock_delay = gesture_config.get("lock_delay", 5)
                lock_hand = gesture_config.get("lock_hand", "Right")

                # =========================
                # HOLD → LOCK 토글
                # =========================
                if open_hand and handedness == lock_hand:

                    if palm_start_time is None:
                        palm_start_time = time.time()

                    elapsed = time.time() - palm_start_time
                    countdown = max(0, lock_delay - elapsed)

                    mode = "HOLDING"

                    # 일정 시간 유지하면 LOCK 토글
                    if elapsed >= lock_delay:
                        lock_mode = not lock_mode
                        palm_start_time = None
                        countdown = 0

                else:
                    palm_start_time = None
                    countdown = 0

                # =========================
                # 볼륨 제어
                # =========================
                if not lock_mode and fist:

                    now = time.time()

                    if now - lastChange > changeDelay:

                        if handedness == gesture_config["volume_up"]:
                            mode = "VOLUME UP"
                            volPercent = min(100, volPercent + 1)

                            last_mode = mode
                            mode_timer = time.time()

                        if handedness == gesture_config["volume_down"]:
                            mode = "VOLUME DOWN"
                            volPercent = max(0, volPercent - 1)

                            last_mode = mode
                            mode_timer = time.time()

                        lastChange = now

                detector.draw(frame, handLms)

        # 최근 상태 유지 (짧게 유지해서 깜빡임 방지)
        if time.time() - mode_timer < mode_duration:
            mode = last_mode

        # =========================
        # LOCK 상태 표시
        # =========================
        if lock_mode:
            mode = "LOCKED"

        volume.set_volume(volPercent)

        # =========================
        # FPS 계산
        # =========================
        cTime = time.time()
        fps = 1 / max((cTime - pTime), 0.001)
        pTime = cTime

        draw_ui(frame, mode, volPercent, fps, lock_mode, countdown)
        cv2.imshow("Gesture Control", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

        # 창 닫힘 감지
        try:
            if cv2.getWindowProperty("Gesture Control", cv2.WND_PROP_VISIBLE) < 1:
                break
        except:
            break

    cap.release()
    cv2.destroyAllWindows()