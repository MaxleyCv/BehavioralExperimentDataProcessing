from abc import ABC
from typing import List, Optional, Callable, Any


class SelectorFunction(ABC):
    """
    Interface for selector functions per video.
    Please inherit and set up for each detection.
    You need to inherit it in f1.py, f2.py, etc. You also need to import those into the module's __init__.
    Look up examples in existing files. However, you NEED to select possible points and modify calculations.
    In our example we have a board that is a good reference for most videos.
    An example for it is present in corresponding files for our video
    """
    MANIFEST = """Base class"""

    def top_left(self, detections: List[List[int]]) -> Optional[List[int]]:
        pass

    def top_right(self, detections: List[List[int]]) -> Optional[List[int]]:
        pass

    def bottom_left(self, detections: List[List[int]]) -> Optional[List[int]]:
        pass

    def bottom_right(self, detections: List[List[int]]) -> Optional[List[int]]:
        pass
