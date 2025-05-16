import cv2
import numpy as np

from timestamps_from_videos.timestamp_reader import VideoTimestampReader


class FirstVideoTimestampReader(VideoTimestampReader):
    def get_timestamp_image(self, frame: np.array) -> np.ndarray:
        # doing some convolution here
        kernel = np.array(
            [
                [1, 1, 1],
                [1, 4, 1],
                [1, 1, 1]
            ]
        ) / 12
        # Need to be in grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame[0:25, 125:250]
        # For this particular video I needed black-on-white
        frame[frame > 210] = 0
        frame[frame > 10] = 255

        frame = cv2.filter2D(frame, ddepth=-1, kernel=kernel)
        # returning filtered image
        frame[frame < int(2 / 3 * 255) + 1] = 0

        return frame