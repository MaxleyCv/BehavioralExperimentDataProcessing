import os
from queue import Queue

from dependencies.dependency import Dependency
from routines.constants import Context
from routines.video_calibration_routine import VideoCalibrationRoutine


class TransformsPresentDependency(Dependency):
    def __init__(self, routine_queue: Queue):
        context = Context()
        self.number_of_videos = context.NUMBER_OF_VIDEOS
        self.__context = context
        super().__init__(routine_queue, [
            (self.all_transforms_present, VideoCalibrationRoutine(self.number_of_videos)),
        ])

    def all_transforms_present(self) -> bool:
        homography_paths = set(f"{i}.homography" for i in range(self.number_of_videos))
        all_homographies_present = set(os.listdir(self.__context.HOMOGRAPHY_ROOT_FOLDER)).issuperset(homography_paths)
        return all_homographies_present
