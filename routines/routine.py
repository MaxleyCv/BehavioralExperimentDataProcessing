from abc import ABC

class Routine(ABC):
    """
    Setup routine base class (abstract) to guide config file
    """
    def execute(self):
        pass
