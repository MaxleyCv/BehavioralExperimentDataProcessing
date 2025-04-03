from routines.routine import Routine

class ErrorRoutine(Routine):
    """
    This is just a routine to produce an error response in the dependency if such cannot be executed.
    """
    def __init__(self):
        pass

    def execute(self):
        raise NotImplementedError(
            "Current dependency cannot be resolved without your intervention!"
        )