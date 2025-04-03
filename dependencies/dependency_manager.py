from queue import Queue
from typing import List, Type

from dependencies.abstract_dependency import AbstractDependency
from routines.routine import Routine


class DependencyManager:
    def __init__(
            self,
            dependency_list: List[Type[AbstractDependency]],
            current_routine: Routine
    ):
        routine_additional_queue = Queue()
        self.dependency_list = [dependency(routine_queue=routine_additional_queue) for dependency in dependency_list]
        self.__current_routine = current_routine
        self.__routine_queue = routine_additional_queue

    def all(self) -> bool:
        resolution = True

        for dependency in self.dependency_list:
            resolution = resolution and dependency.met()

        return resolution

    def resolve_all(self) -> None:
        for dependency in self.dependency_list:
            dependency.resolve()
        self.__routine_queue.put(self.__current_routine)
        while self.__routine_queue.not_empty:
            next_routine = self.__routine_queue.get()
            next_routine.execute()
        return None
