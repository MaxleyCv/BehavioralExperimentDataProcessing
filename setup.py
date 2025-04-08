from routines.decompose_video_routine import DecomposeVideoRoutine
from routines.pose_generation_routine import PoseGenerationRoutine
from routines.routine_manager import RoutineManager
from routines.video_calibration_routine import VideoCalibrationRoutine

if __name__ == '__main__':
    routine_manager = RoutineManager(
        [DecomposeVideoRoutine()]
    )
    routine_manager.exec()
