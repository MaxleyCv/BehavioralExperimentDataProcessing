from collections import defaultdict

import cv2
import numpy as np


class VideoAssigner:
    """
    This is just a visualization tool to show a particular person where the identity is missed.
    Normally I would use 'd' for deleted frames.
    """
    def __init__(self, vid_path):
        self.__vid_path = vid_path
        self.assignment_data = defaultdict(list)

    def __frame(self, number: int) -> cv2.Mat | np.ndarray:
        """
        Returning the frame from the decomposed video.
        :param number: frame_id, used by the decomposer
        :return:
        """
        return cv2.imread(self.__vid_path + f"/{number}.png")

    def show_skeleton(self, number, trackable_instance) -> None:
        frame = self.__frame(number)
        for point in trackable_instance.skeleton:
            cv2.circle(frame, list(map(int, point)), 2, (255, 255, 0), 2)
        cv2.imshow("frame", frame)
        key = cv2.waitKey(0)
        self.assignment_data[str(key)].append(trackable_instance)
        cv2.destroyAllWindows()
        return None
