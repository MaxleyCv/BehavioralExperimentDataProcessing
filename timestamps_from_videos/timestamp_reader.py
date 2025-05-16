from abc import ABC

import cv2
import numpy as np
from pytesseract import pytesseract


class VideoTimestampReader(ABC):
    def get_timestamp_image(self, frame: np.array) -> np.ndarray:
        """
        This is actually the only preprocessing step that is needed to be hardcoded.
        Timestamp serialization will be handled automatically by this parent class.
        :param frame:
        :return:
        """
        pass

    def produce_timestamp(self, frame: np.array) -> str:
        """
        This uses tesseract to produce a timestamp from a frame that is provided in the video.
        Note: This class is made specifically for Foscam C1 cameras
        :param frame:
        :return:
        """
        subframe = self.get_timestamp_image(frame)
        serialized_text = pytesseract.image_to_string(subframe, timeout=2)
        res = serialized_text[:-1] # crop \n
        if res == "":
            res = "null"
        return res
