from typing import Callable

from dependencies.dependency_manager import DependencyManager



class DependencyReliantRoutineMixin:
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager


def dependency_reliant_method(method: Callable) -> Callable:
    """
    For class methods (e.g. routine-based execution) which require dependency routines to be met.
    :param method: method of the routine, e.g. execute
    :return:
    """
    def wrapper(this: DependencyReliantRoutineMixin, *args, **kwargs):
        all_conditions_are_met: bool = this.dependency_manager.all()
        if not all_conditions_are_met:
            this.dependency_manager.resolve_all()
        return method(this, *args, **kwargs)

    return wrapper
