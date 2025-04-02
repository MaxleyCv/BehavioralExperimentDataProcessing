from typing import List

from routines.routine import Routine


class RoutineManager:
    def __init__(self, routine_list: List[Routine]):
        self.__routine_list = routine_list
        self.status = True

    def exec(self) -> bool:
        for routine in self.__routine_list:
            self.status = self.status and routine.execute()
        return self.status