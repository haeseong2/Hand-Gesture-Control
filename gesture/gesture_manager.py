from gesture.volume_gesture import VolumeGesture
from gesture.lock_gesture import LockGesture

class GestureManager:

    def __init__(self, config):
        self.volume = VolumeGesture(config)
        self.lock = LockGesture(config)

    def process(self, hand_data):

        vol_result = self.volume.process(hand_data)
        lock_result = self.lock.process(hand_data)

        return {
            "mode": vol_result.get("mode", ""),
            "countdown": lock_result.get("countdown", 0),
            "lock_mode": self.lock.lock_mode
        }