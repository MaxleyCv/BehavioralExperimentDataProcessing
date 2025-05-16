import os
from queue import Queue

from dependencies.dependency import Dependency
from routines.constants import Context
from routines.pose_generation_routine import PoseGenerationRoutine


class PosesYieldedDependency(Dependency):
    def __init__(self, routine_queue: Queue):
        context = Context()
        self.__context = context
        super().__init__(routine_queue, [
            (self.poses_yielded_condition, PoseGenerationRoutine())
        ])

    def poses_yielded_condition(self):
        return len(os.listdir(self.__context.POSE_ROOT_FOLDER)) == self.__context.NUMBER_OF_VIDEOS
