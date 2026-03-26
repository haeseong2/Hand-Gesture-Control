import cv2

def get_camera():

    for i in range(5):

        print(f"카메라 {i} 시도중...")

        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) 

        if cap.isOpened():
            print(f"카메라 {i} 연결 성공")
            return cap

        cap.release()

    print("No camera found")
    return None