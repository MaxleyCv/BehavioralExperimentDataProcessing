import csv
import os
import pickle
from collections import defaultdict
from typing import List

from routines.constants import Context
from routines.routine import Routine
from utils.command_line_interface import CommandInterface
from utils.timing import UET


class ComposeTimestampsRoutine(Routine):
    """
    The whole idea is to write the timestamps into UETs from video.
    """
    def __init__(self):
        self.__context = Context()
        self.__get_status()

    def __get_status(self):
        self.__timestamps_present = len(os.listdir(
            self.__context.TIMESTAMP_ROOT_FOLDER
        )) == self.__context.NUMBER_OF_VIDEOS
        # this goes first as the first priority
        self.__prepared_timestamps_present = len(
            os.listdir(
                self.__context.UET_ROOT_FOLDER
            )
        ) == self.__context.NUMBER_OF_VIDEOS

    def __prepare_timestamps_from_strings(self, strings_file_path: str) -> List[UET]:
        with open(strings_file_path, "r") as strings_file:
            reader = csv.reader(strings_file)
            result = []
            stamps_seen = defaultdict(lambda : -1)
            all_timestamps = []

            for row in reader:
                all_timestamps.append(row[0])

            for timestamp in all_timestamps:
                if timestamp != 'null':
                    stamps_seen[timestamp] += 1
                padding = 10 ** 6 // all_timestamps.count(timestamp)
                # a little bit inefficient memory-wise but ok in terms of readability
                result.append(UET(timestamp) + padding * stamps_seen[timestamp])

        return result

    def execute(self) -> bool:
        cmd = CommandInterface("Starting composing your timestamps!")
        if self.__prepared_timestamps_present:
            return True
        strings_folder = self.__context.EXTRA_TIMESTAMPS_FOLDER
        if self.__timestamps_present:
            strings_folder = self.__context.TIMESTAMP_ROOT_FOLDER

        for video_id in range(self.__context.NUMBER_OF_VIDEOS):
            timestamps = self.__prepare_timestamps_from_strings(
                strings_folder + f"{video_id}.csv"
            )
            with open(self.__context.UET_ROOT_FOLDER + f"{video_id}.uets", "wb") as uet_file:
                pickle.dump(timestamps, uet_file)
        return True
