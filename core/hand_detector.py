import mediapipe as mp
import math

class HandDetector:

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils

    def get_distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def detect(self, frame):
        imgRGB = frame[:, :, ::-1]
        results = self.hands.process(imgRGB)

        if not results.multi_hand_landmarks:
            return None

        handLms = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label.lower()

        lmList = [(lm.x, lm.y) for lm in handLms.landmark]

        palm = lmList[0]
        tipIds = [4, 8, 12, 16, 20]

        fingers = []

        for tip in tipIds:
            tip_dist = self.get_distance(lmList[tip], palm)
            pip_dist = self.get_distance(lmList[tip - 2], palm)

            diff = tip_dist - pip_dist

            fingers.append(1 if diff > 0.02 else 0)

        finger_count = sum(fingers)

        # 안정 조건
        fist = finger_count <= 2
        open_hand = finger_count >= 4

        return {
            "fist": fist,
            "open_hand": open_hand,
            "fingers": finger_count,
            "hand": handedness,
            "handLms": handLms
        }

    def draw(self, frame, hand_data):
        if not hand_data:
            return

        self.mpDraw.draw_landmarks(
            frame,
            hand_data["handLms"],
            self.mpHands.HAND_CONNECTIONS
        )