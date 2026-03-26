import pyautogui
import time

class MouseGesture:
    """
    손 위치로 마우스 이동 + 검지/중지 붙이면 클릭
    """

    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.last_click_time = 0
        self.click_delay = 0.5

    def process(self, hand_data):

        # 손 데이터 없으면 종료
        if hand_data is None:
            return None

        lm = hand_data.get("landmarks")
        if lm is None:
            return None

        # 검지 위치
        x = lm[8].x
        y = lm[8].y

        screen_x = int(x * self.screen_w)
        screen_y = int(y * self.screen_h)

        # 마우스 이동
        pyautogui.moveTo(screen_x, screen_y)

        # 클릭 감지
        index_tip = lm[8]
        middle_tip = lm[12]

        dist = ((index_tip.x - middle_tip.x) ** 2 +
                (index_tip.y - middle_tip.y) ** 2) ** 0.5

        now = time.time()

        if dist < 0.05 and now - self.last_click_time > self.click_delay:
            pyautogui.click()
            self.last_click_time = now
            return "CLICK"

        return "MOVE"