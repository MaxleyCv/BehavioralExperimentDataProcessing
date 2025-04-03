from routines.pose_generation_routine import PoseGenerationRoutine
from routines.routine_manager import RoutineManager
from routines.video_calibration_routine import VideoCalibrationRoutine

if __name__ == '__main__':
    routine_manager = RoutineManager(
        [PoseGenerationRoutine(1)]
    )
    routine_manager.exec()
