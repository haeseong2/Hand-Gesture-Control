import time

class VolumeGesture:

    def __init__(self, config):
        self.config = config
        self.volPercent = 50
        self.lastChange = 0
        self.delay = 0.30
        self.fist_count = 0

    def process(self, hand_data):

        if not hand_data:
            self.fist_count = 0
            return {"mode": ""}

        if hand_data.get("fist"):
            self.fist_count += 1
        else:
            self.fist_count = 0
            return {"mode": ""}

        # 3프레임 유지
        if self.fist_count < 3:
            return {"mode": ""}

        now = time.time()

        if now - self.lastChange < self.delay:
            return {"mode": ""}

        hand = hand_data.get("hand")

        if hand == self.config["volume_up"]:
            self.volPercent = min(150, self.volPercent + 2)
            mode = "VOLUME UP"

        elif hand == self.config["volume_down"]:
            self.volPercent = max(0, self.volPercent - 2)
            mode = "VOLUME DOWN"

        else:
            mode = ""

        self.lastChange = now
        return {"mode": mode}