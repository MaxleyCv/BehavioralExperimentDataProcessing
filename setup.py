from routines.routine_manager import RoutineManager
from routines.video_calibration_routine import VideoCalibrationRoutine

if __name__ == '__main__':
    routine_manager = RoutineManager(
        [VideoCalibrationRoutine(4)]
    )
    routine_manager.exec()
