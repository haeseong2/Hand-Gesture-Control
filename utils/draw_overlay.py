"""
[draw_ui]
카메라 위에 UI 출력
"""

import cv2

def draw_ui(frame, mode, vol, fps, lock_mode, countdown):

    h, w, _ = frame.shape
    center = w // 2

    if mode:
        cv2.putText(frame, mode,
                    (center - 150, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (255, 255, 0),
                    3)

    if lock_mode:
        cv2.putText(frame, "LOCK MODE",
                    (center - 150, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3)

    if countdown > 0:
        cv2.putText(frame, f"{countdown:.1f}s",
                    (w - 120, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3)

    cv2.putText(frame, f"FPS {int(fps)}",
                (w - 120, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2)

    cv2.rectangle(frame, (center - 250, h - 120), (center + 250, h - 80), (50,50,50), -1)
    cv2.rectangle(frame, (center - 250, h - 120),
                  (center - 250 + int(vol*5), h - 80),
                  (0,255,0), -1)