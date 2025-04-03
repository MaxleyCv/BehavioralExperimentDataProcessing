from abc import ABC
from queue import Queue


class AbstractDependency(ABC):
    def __init__(self, routine_queue: Queue):
        pass

    def met(self, *args, **kwargs):
        pass

    def resolve(self):
        pass
