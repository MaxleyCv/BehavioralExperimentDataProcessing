import os
from queue import Queue

from dependencies.dependency import Dependency
from routines.constants import Context
from routines.error_routine import ErrorRoutine


class VideoPresentDependency(Dependency):
    def __init__(self, number_of_videos: int, routine_queue: Queue):
        self.__context = Context()
        self.number_of_videos = number_of_videos
        super().__init__(routine_queue, [(self.all_videos_present_condition, ErrorRoutine())])

    def resolve(self, *args, **kwargs):
        raise NotImplementedError(
            "This video can only be resolved by adding data!"
        )

    def all_videos_present_condition(self) -> bool:
        video_paths = set(f"{i}.mp4" for i in range(self.number_of_videos))
        all_videos_present =  set(os.listdir(self.__context.VIDEO_ROOT_FOLDER)).issuperset(video_paths)
        return all_videos_present
