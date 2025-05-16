import math
import pickle
from typing import List

from routines.constants import Context
from routines.routine import Routine
from utils.timing import UET
from visual_tools.person_representation import PersonRepresentation


class CombineVisualFeaturesRoutine(Routine):
    def __init__(self):
        self.__context = Context()

    def execute(self) -> bool:
        uet_grid = self.__produce_uet_grid()
        tags = self.__context.keys
        for key in tags:
            person_representation = PersonRepresentation(
                key,
                context=self.__context
            )
            feature_vectors = person_representation.produce_feature_vectors(uet_grid)
            with open(
                self.__context.VISUAL_EMBEDDINGS_COMBINED_PATH + key + ".emb", 'wb'
            ) as f:
                pickle.dump(feature_vectors, f)
        self.__save_uet_grid(uet_grid)
        return True

    def __produce_uet_grid(self) -> List[UET]:
        minimal_timestamp = min(
            map(
                min, [
                    self.__read_uet_files(video_id)[self.__context.TIMESTAMP_CUTOFF_FRAMES[video_id]:]
                    for video_id in range(self.__context.NUMBER_OF_VIDEOS)
                ]
            )
        )
        maximal_timestamp = max(
            map(
                max, [
                    self.__read_uet_files(video_id)[self.__context.TIMESTAMP_CUTOFF_FRAMES[video_id]:]
                    for video_id in range(self.__context.NUMBER_OF_VIDEOS)
                ]
            )
        )
        uet_grid = (
            list(
                map(
                    UET.from_integer,
                    range(minimal_timestamp, maximal_timestamp + 1, self.__context.TIME_STEP_INTERVAL_USECONDS)
                )
            )
        )
        return uet_grid

    def __read_uet_files(self, video_id: int) -> List[UET]:
        with open(self.__context.UET_ROOT_FOLDER + f"{video_id}.uets", "rb") as f:
            timestamps = pickle.load(f)
        return timestamps

    def __save_uet_grid(self, uet_grid: List[UET]) -> None:
        with open(self.__context.UET_GRID_FILE, 'wb') as f:
            pickle.dump(uet_grid, f)
        return None
