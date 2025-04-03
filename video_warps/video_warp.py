import pickle
from typing import List, Dict

import cv2
import numpy as np

from routines.constants import Context
from video_warps.selector_function import SelectorFunction


class VideoWarp:
    """
    A class to descend from for matrix warp calculation for floor coordinates.
    Everything is based on your detection capabilities and what you put into the functions themselves.
    Used by VideoCalibrationRoutine
    """
    DESTINATION_COORDINATES = np.array([
        [0, 0],
        [1280, 720],
        [0, 720],
        [1280, 0]
    ], np.float32)

    def __init__(
            self,
            context: Context,
            detection_array: List,
            selector_function: SelectorFunction,
            file_id: int
    ):
        self.__detections = detection_array
        self.__selector_function = selector_function
        self.__file_id = file_id
        self.__context = context
        self.__calculate_matrix_warp()

    def __calculate_matrix_warp(self) -> None:
        """
        Calculating matrix warp to map to (0,0), (720, 1280) coordinates
        :return: None
        """
        source_coordinates = np.array([
            self.__selector_function.top_left(self.__detections),
            self.__selector_function.bottom_right(self.__detections),
            self.__selector_function.bottom_left(self.__detections),
            self.__selector_function.top_right(self.__detections)
        ], dtype=np.float32)

        homography = cv2.getPerspectiveTransform(source_coordinates, self.DESTINATION_COORDINATES)
        with open(f"{self.__context.HOMOGRAPHY_ROOT_FOLDER}{self.__file_id}.homography", 'wb') as file:
            pickle.dump(homography, file)
        return None
