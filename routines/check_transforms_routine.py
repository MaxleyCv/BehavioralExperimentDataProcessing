import os
import pickle

import cv2

from routines.constants import Context
from routines.routine import Routine


class VideoTransformShowcaseRoutine(Routine):
    def __init__(self):
        self.__context = Context()

    def execute(self):
        number_of_videos = len(
            os.listdir(self.__context.HOMOGRAPHY_ROOT_FOLDER)
        )
        for i in range(number_of_videos):
            capture = cv2.VideoCapture(self.__context.VIDEO_ROOT_FOLDER + f"{i}.mp4")
            _, frame = capture.read()
            with open(f"{self.__context.HOMOGRAPHY_ROOT_FOLDER}{i}.homography", 'rb') as file:
                transform = pickle.load(file)
                frame = cv2.warpPerspective(frame, transform, (frame.shape[1], frame.shape[0]))
                cv2.imshow(f"Showing warp of {i}.mp4", frame)
