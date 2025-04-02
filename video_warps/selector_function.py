from abc import ABC
from typing import List, Optional, Callable, Any


class SelectorFunction(ABC):
    """
    Interface for selector functions per video.
    Please inherit and set up for each detection.
    You need to inherit it in 1.py, 2.py, etc.
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
