import numpy as np
from window_capture import screen_record_cv2_mode, screen_record_win32_mode
from pvz_automate import PVZAutomate
from threading import Thread


if __name__ == '__main__':
    windowName = 'CV Output'
    pvzAutomator = PVZAutomate(initial_record_screen=np.array([]), window_name=windowName)
    # t1 = Thread(target=screen_record_cv2_mode, args=(pvzAutomator, windowName))
    # t1.start()
    t2 = Thread(target=screen_record_win32_mode, args=(pvzAutomator, windowName))
    t2.start()
