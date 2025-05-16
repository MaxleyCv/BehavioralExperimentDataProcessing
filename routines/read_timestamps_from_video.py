import csv
import os

import cv2
import numpy as np

from routines.constants import Context
from routines.routine import Routine
from timestamps_from_videos.timestamp_readers import timestamp_readers
from utils.command_line_interface import CommandInterface
from utils.timing import UET


class ReadTimestampsPerVideo(Routine):
    """
    Sometimes you need to read timestamps directly from the video file.
    This will save the timestamps into `extra_timestamps` folder.
    However, you need to still write your timestamp extraction function, as outlined in an example
    """

    def __init__(self):
        self.__context = Context()
        self.__decomposed_video_paths = [
            self.__context.VIDEO_DECOMPOSITION_ROOT_FOLDER + f"{vid_num}/"
            for vid_num
            in range(self.__context.NUMBER_OF_VIDEOS)
        ]

    def execute(self) -> bool:
        command_interface = CommandInterface("Starting production of timestamps!")
        for video_index in range(self.__context.NUMBER_OF_VIDEOS):
            command_interface.write_instruction(f"TIMESTAMPS FOR VIDEO {video_index}")
            reader = timestamp_readers[video_index]
            timestamp_strings = []
            for frame_id in range(len(os.listdir(self.__decomposed_video_paths[video_index]))):
                timestamp_string = reader.produce_timestamp(
                    cv2.imread(self.__context.VIDEO_DECOMPOSITION_ROOT_FOLDER + f"{video_index}/" + f"{frame_id}.png"),
                )
                timestamp_strings.append([timestamp_string])
            target_file_path = self.__context.EXTRA_TIMESTAMPS_FOLDER + f"{video_index}.csv"
            with open(target_file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerows(timestamp_strings)

            command_interface.write_instruction("THESE ARE PROBLEMATIC TIMESTAMPS! FIX MANUALLY!")
            uets = np.array(list(map(lambda ts: UET(ts[0])(), timestamp_strings)))
            uet_deltas = uets[1:] - uets[:-1]

            bad_indexes = [index for index in range(len(uet_deltas)) if uet_deltas[index] < 0]
            command_interface.write_instruction(str(bad_indexes))
        return True
