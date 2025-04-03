from typing import List, Optional, Callable, Any

import numpy as np

from utils.homography import homogenize, dehomogenize_2d
from video_warps.selector_function import SelectorFunction


class FourthSelectorFunction(SelectorFunction):
    MANIFEST = """
    MANIFEST
    0, 1 - board line
    2, 3 - board right window line
    4, 5 - board left window line
    6, 7 - corner to current corner (diagonal)
    8, 9 - parallel to border line
    """

    def __init__(self):
        self.__manifest_completed = False

    @staticmethod
    def __conditional_on_manifest_completed(func: Callable) -> Callable:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            this = args[0]
            if not this.__manifest_completed:
                detections = args[1]
                this.__manifest(args[1])
            return func(*args, **kwargs)
        return wrapped

    def __manifest(self, detections: List[List[int]]) -> None:
        print(self.MANIFEST)
        detections = np.array(list(map(homogenize, detections)))
        self.boardline = np.cross(detections[0], detections[1])
        self.board_right_window_line = np.cross(detections[2], detections[3])
        self.board_left_window_line = np.cross(detections[4], detections[5])
        self.corner_current_line = np.cross(detections[6], detections[7])
        self.parallel_to_border_line = np.cross(detections[8], detections[9])
        self.__manifest_completed = True

    @__conditional_on_manifest_completed
    def top_left(self, detections: List[List[int]]) -> Optional[List[int]]:
        top_left = np.cross(
            self.boardline,
            self.board_right_window_line
        )
        return dehomogenize_2d(top_left)

    @__conditional_on_manifest_completed
    def top_right(self, detections: List[List[int]]) -> Optional[List[int]]:
        p_inf = np.cross(
            self.boardline,
            self.parallel_to_border_line
        )
        bottom_right = np.cross(
            self.board_left_window_line,
            self.corner_current_line
        )
        window_infinity_line = np.cross(
            bottom_right, p_inf
        )
        top_right = np.cross(self.board_right_window_line, window_infinity_line)
        return dehomogenize_2d(top_right)

    @__conditional_on_manifest_completed
    def bottom_left(self, detections: List[List[int]]) -> Optional[List[int]]:
        bottom_left = np.cross(
            self.boardline,
            self.board_left_window_line
        )
        return dehomogenize_2d(bottom_left)

    @__conditional_on_manifest_completed
    def bottom_right(self, detections: List[List[int]]) -> Optional[List[int]]:
        bottom_right = np.cross(
            self.board_left_window_line,
            self.corner_current_line
        )
        return dehomogenize_2d(bottom_right)
