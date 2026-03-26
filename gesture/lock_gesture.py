import time

class LockGesture:

    def __init__(self, config):
        self.config = config
        self.lock_mode = False
        self.start_time = None
        self.open_count = 0

    def process(self, hand_data):

        if not hand_data:
            self.start_time = None
            self.open_count = 0
            return {"countdown": 0}

        if hand_data.get("open_hand"):
            self.open_count += 1
        else:
            self.open_count = 0
            self.start_time = None
            return {"countdown": 0}

        # 3프레임 유지
        if self.open_count < 3:
            return {"countdown": 0}

        if hand_data.get("hand") != self.config["lock_hand"]:
            self.start_time = None
            return {"countdown": 0}

        if self.start_time is None:
            self.start_time = time.time()

        elapsed = time.time() - self.start_time
        delay = self.config.get("lock_delay", 3)

        if elapsed >= delay:
            self.lock_mode = not self.lock_mode
            self.start_time = None

        return {"countdown": max(0, delay - elapsed)}