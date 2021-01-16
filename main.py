# initial
import numpy as np

# Multithreading to make it faster and concurrently profile CV version and win32 version
from threading import Thread

# For the Automation
from computer_vision_handler import CVToAutomationInterfaceClass
from pvz_automate import PVZAutomate

if __name__ == '__main__':
    windowName = 'CV Output'

    # Initialize relevant classes for code abstraction
    pvzAutomator = PVZAutomate(window_name=windowName)
    automationInterface = CVToAutomationInterfaceClass(automator=pvzAutomator, window_name=windowName,
                                                       should_visualize=True, should_profile=False)

    # t1 = Thread(target=screen_record_cv2_mode, args=(pvzAutomator, windowName))
    # t1.start()

    t2 = Thread(target=automationInterface.screen_record_win32_mode)
    t2.start()
