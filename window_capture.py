# Profiling
import time

# Screen Recording
import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from PIL import ImageGrab

# Automation
from pvz_automate import PVZAutomate


def screen_record_win32_mode(automator: PVZAutomate, window_name: str = 'CV Output'):
    last_time = time.time()
    winCap = WindowCapture('Plants vs. Zombies')
    while True:
        # Record Screen using win32 and process if needed
        printScreen = np.array(winCap.get_screenshot())
        # processedImage = process_img(printScreen)

        # Performance Profiling
        print('Win32 mode working at {} loops per second.'.format(1.0 / (time.time() - last_time)))
        last_time = time.time()

        # Update working class and apply working Logic
        automator.printScreen = printScreen
        automator.working_logic()

        # Visualize what the automator is seeing
        cv2.imshow(winname=window_name, mat=automator.printScreen)
        # cv2.imshow(winname=window_name, mat=cv2.imread('lawn.png'))

        # User Input and Termination condition
        automator.user_input_detect()
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def screen_record_cv2_mode(automator: PVZAutomate, window_name: str = 'CV Output'):
    last_time = time.time()
    while True:
        # Record Screen using OpenCV (800x600 windowed mode) and process if needed
        printScreen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        # processedImage = process_img(printScreen)

        # Performance Profiling
        print('OpenCV mode Working at {} loops per second.'.format(1.0 / (time.time() - last_time)))
        last_time = time.time()

        # Update working class and apply working Logic
        automator.printScreen = cv2.cvtColor(printScreen, cv2.COLOR_BGR2RGB)
        automator.working_logic()

        # Visualize what the automator is seeing
        cv2.imshow(winname=window_name, mat=automator.printScreen)
        # cv2.imshow(winname=window_name, mat=cv2.imread('lawn.png'))

        # User Input and Termination condition
        automator.user_input_detect()
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def list_window_names():
    def win_enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(win_enum_handler, None)


class WindowCapture:
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and title-bar and cut them off
        border_pixels = 8
        titleBar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titleBar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titleBar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[..., :3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y
