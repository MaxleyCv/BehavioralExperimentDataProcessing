from typing import Optional, List

import cv2

from routines.constants import Context
from routines.routine import Routine
from utils.command_line_interface import CommandInterface


class DecomposeVideoRoutine(Routine):
    """
    This routine will support decomposition of the videos into individual frames.
    This is needed by an identity assignment routine as it depends on the frame itself.
    """
    def __init__(self):
        self.__context = Context()
        self.__number_of_videos: int = self.__context.NUMBER_OF_VIDEOS
        self.__video_paths: List[str] = [self.__context.VIDEO_ROOT_FOLDER + f"{i}.mp4" for i in range(self.__number_of_videos)]
        self.__decomposition_paths: List[str] = [
            self.__context.VIDEO_DECOMPOSITION_ROOT_FOLDER + f"{i}/" for i in range(self.__number_of_videos)
        ]
        self.__interface: Optional[CommandInterface] = None

    def execute(self) -> bool:
        self.__interface = CommandInterface("Starting video decompositions!")
        status = True
        for path, decomposition_path in zip(self.__video_paths, self.__decomposition_paths):
            status = status and self.__produce_individual_frames_by_video(path, decomposition_path)
        return status

    def __produce_individual_frames_by_video(self, video_path: str, decomposition_path: str) -> bool:
        self.__interface.write_instruction(f"Starting decomposition of {video_path}")

        capture = cv2.VideoCapture(video_path)
        index_in: int = -1

        full_video_length: int = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        self.__interface.write(f"Current progress: 0/{full_video_length}")

        while True:
            success: bool = capture.grab()
            if not success: break
            index_in += 1
            success, frame = capture.retrieve()
            if not success: break
            cv2.imwrite(f'{decomposition_path}{index_in}.png', frame)
            self.__interface.write(f"Current progress: {index_in + 1}/{full_video_length}")

        self.__interface.write_instruction("Finished current video.")

        return True
