"""
[draw_ui]
텍스트 기반 UI 출력 (아이콘 제거 버전)

frame       : 카메라 프레임
mode        : 현재 상태 (VOLUME UP / DOWN / HOLDING / LOCKED)
volPercent  : 볼륨 값 (0~100)
fps         : FPS 값
lock_mode   : LOCK 상태 여부
countdown   : LOCK까지 남은 시간
"""

import cv2

def draw_ui(frame, mode, volPercent, fps, lock_mode=False, countdown=0):

    h, w, _ = frame.shape
    center = w // 2

    # 상태 텍스트 (크게 중앙)
    if mode != "":
        cv2.putText(frame,
                    mode,
                    (center - 200, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.3,
                    (0, 255, 255),
                    3)

    # FPS (오른쪽 위 / 작게 / 빨간색)
    cv2.putText(frame,
                f"FPS {int(fps)}",
                (w - 140, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2)

    # 카운트다운 (파란색 / 진하게)
    if countdown > 0:
        cv2.putText(frame,
                    f"{countdown:.1f}s",
                    (w - 140, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3)

    # 볼륨 바 배경
    cv2.rectangle(frame,
                  (center - 250, h - 120),
                  (center + 250, h - 80),
                  (50, 50, 50),
                  -1)

    # 볼륨 채우기
    cv2.rectangle(frame,
                  (center - 250, h - 120),
                  (center - 250 + int(volPercent * 5), h - 80),
                  (0, 255, 0),
                  -1)

    # 볼륨 텍스트 (크게 초록색)
    cv2.putText(frame,
                f"VOLUME {volPercent}%",
                (center - 160, h - 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3)