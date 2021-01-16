import cv2
import numpy as np
from random import uniform
from pyautogui import click
from typing import List


class ImageProcessor:
    @staticmethod
    def edge_detection(image: np.ndarray) -> np.ndarray:
        # convert to gray
        processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # edge detection
        processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=200)
        processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
        return processed_img

    @staticmethod
    def match_and_find(component_name: str, screen_to_be_analysed: np.ndarray):
        croppedImage = cv2.imread(component_name + '.png')
        croppedWidth = croppedImage.shape[1] + 10
        croppedHeight = croppedImage.shape[0] + 10
        result = cv2.matchTemplate(screen_to_be_analysed, croppedImage, cv2.TM_CCOEFF_NORMED)
        return croppedHeight, croppedWidth, result


class PVZAutomate:
    def __init__(self, initial_record_screen: np.ndarray, window_name: str = 'CV Output'):
        self.windowName = window_name
        self.printScreen = initial_record_screen
        self.processedResultImage = self.printScreen
        self.startFlag = False

    def input_click(self, coordinates: tuple, click_chance: float = 1, should_show: bool = False):
        if uniform(0, 1) <= click_chance:
            click(coordinates[0], coordinates[1])
        if should_show:
            cv2.imshow(self.windowName, self.processedResultImage)

    def user_input_detect(self):
        # User Control Menu
        if cv2.waitKey(5) & 0xFF == ord('s'):
            cv2.imwrite('seed.png', self.printScreen)
            cv2.imwrite('processed_sun.png', img=ImageProcessor.edge_detection(self.printScreen))
        if cv2.waitKey(5) & 0xFF == ord('b'):
            self.startFlag = True
        if cv2.waitKey(5) & 0xFF == ord('e'):
            self.startFlag = False

    def detect_components(self, component_name: str, threshold: float = 0, color: tuple = (0, 255, 0)) \
            -> [np.ndarray, List[tuple]]:
        croppedHeight, croppedWidth, result = ImageProcessor.match_and_find(component_name, self.printScreen)

        # Calculate outputs
        clickCoordinatesList, processedResultImage = [], self.printScreen
        # If confidence is greater than threshold, it is a valid match.
        loc = np.where(result >= threshold)
        for location_point in zip(*loc[::-1]):
            # Bounding Boxes
            detected_topLeft = location_point
            detected_bottomRight = (location_point[0] + croppedWidth, location_point[1] + croppedHeight)

            # Calculation of where to click from Bounding box vertices.
            clickCoordinates = ((detected_topLeft[0] + detected_bottomRight[0]) / 2,
                                (detected_topLeft[1] + detected_bottomRight[1]) / 2)
            clickCoordinatesList.append(clickCoordinates)

            # Draws Bounding Box
            processedResultImage = cv2.rectangle(processedResultImage, pt1=detected_topLeft, pt2=detected_bottomRight,
                                                 color=color, thickness=2, lineType=cv2.LINE_4)

        return processedResultImage, clickCoordinatesList

    def detect_component(self, component_name: str, color: tuple = (0, 255, 0)) -> [np.ndarray, tuple]:
        croppedHeight, croppedWidth, result = ImageProcessor.match_and_find(component_name, self.printScreen)

        # Calculate outputs
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val)

        # Bounding Boxes
        detected_topLeft = max_loc
        detected_bottomRight = (max_loc[0] + croppedWidth, max_loc[1] + croppedHeight)

        # Calculation of where to click from Bounding box vertices.
        clickCoordinates = ((detected_topLeft[0] + detected_bottomRight[0]) / 2,
                            (detected_topLeft[1] + detected_bottomRight[1]) / 2)

        # Draws Bounding Box
        processedResultImage = cv2.rectangle(self.printScreen, pt1=detected_topLeft, pt2=detected_bottomRight,
                                             color=color, thickness=2, lineType=cv2.LINE_4)
        return processedResultImage, clickCoordinates

    def collect_sun(self, should_show: bool = False):
        # processedResultImage, clickCoordinatesList = self.detect_components('sun', threshold=0.8)
        # print(len(clickCoordinatesList))
        # for clickCoordinates in clickCoordinatesList:
        #     self.input_click(clickCoordinates)

        self.processedResultImage, clickCoordinates = self.detect_component('sun')
        self.input_click(clickCoordinates)

    def plant(self, click_chance: float = 1, should_show: bool = False):
        if uniform(0, 1) <= click_chance:
            # Choose Seed
            self.processedResultImage, clickCoordinates = self.detect_component('seed')
            self.input_click(clickCoordinates)

            # Plant on lawn
            self.processedResultImage, clickCoordinates = self.detect_component('lawn')
            self.input_click(clickCoordinates)

    def working_logic(self):
        # Auto click detected sun
        if self.startFlag:
            self.collect_sun(should_show=True)
            self.plant(0.25)

