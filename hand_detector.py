import mediapipe as mp

class HandDetector:

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils

    def detect(self, frame):
        imgRGB = frame[:,:,::-1]
        results = self.hands.process(imgRGB)

        return results


    def draw(self, frame, handLms):
        self.mpDraw.draw_landmarks(
            frame,
            handLms,
            self.mpHands.HAND_CONNECTIONS
        )