from typing import List, Any

import cv2
from functools import partial

import numpy as np


class Capture:
    """
    A helper class to capture specific points on the floor to map them further into a decart coordinates.
    Of course there is a level of approximation after the warp but when normalized by full area this works quite well.
    """
    def __init__(self, window: str, frame: np.array):
        """
        Initializing detections of mouse clicks
        """
        self.__detections = []
        cv2.namedWindow(window)
        cv2.imshow(window, frame)
        cv2.setMouseCallback(window, self())

    @property
    def detections(self) -> List[List[int]]:
        return self.__detections[0]

    @staticmethod
    def capture_mouse_clicked(
            event: int, x: int, y: int, flags: Any, param: Any, passthrough=List[List], passthrough_id: int = 0
    ):
        if event == cv2.EVENT_LBUTTONDOWN:
            passthrough[passthrough_id].append([x, y])

    def __call__(self, *args, **kwargs):
        """
        A unified callback event for each detection / video
        :param args: not used
        :param kwargs: not used
        :return: callback event for opencv
        """
        passthrough_id = len(self.__detections)
        self.__detections.append([])
        event_callback = partial(Capture.capture_mouse_clicked, passthrough_id=passthrough_id, passthrough=self.__detections)
        return event_callback
