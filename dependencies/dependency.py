from queue import Queue
from typing import Callable, Tuple, List, Optional

from dependencies.abstract_dependency import AbstractDependency
from routines.routine import Routine


class Dependency(AbstractDependency):
    """
    This ensures that the dependencies are met when running a specific routine.
    While not calling a specific routine outright, it can be useful to understand which routines are required.
    """
    def __init__(
            self,
            routine_queue: Queue,
            condition_routine_mapping: List[Tuple[Callable, Optional[Routine]]]
    ):
        super().__init__(routine_queue)
        self.__routine_queue = routine_queue
        self.__condition_routine_mapping = condition_routine_mapping

    def met(self, *args, **kwargs) -> bool:
        result = True
        for condition, routine in self.__condition_routine_mapping:
            result = result and condition()
        return result

    def resolve(self, *args, **kwargs):
        for condition, routine in self.__condition_routine_mapping:
            if not condition():
                self.__routine_queue.put(routine)
        return self
