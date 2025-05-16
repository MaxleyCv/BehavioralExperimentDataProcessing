from routines.check_extra_timestamps_routine import CheckExtraTimestampsRoutine
from routines.combine_network_and_visual_routine import CombineNetworkAndVisualRoutine
from routines.combine_visual_features_routine import CombineVisualFeaturesRoutine
from routines.compose_timestamps_routine import ComposeTimestampsRoutine
from routines.create_network_features_routine import CreateNetworkFeaturesRoutine
from routines.decompose_video_routine import DecomposeVideoRoutine
from routines.pose_generation_routine import PoseGenerationRoutine
from routines.read_timestamps_from_video import ReadTimestampsPerVideo
from routines.routine_manager import RoutineManager
from routines.trackable_assignment_routine import TrackableAssignmentRoutine

if __name__ == '__main__':
    routine_manager = RoutineManager(
        [
            CombineVisualFeaturesRoutine(), CombineNetworkAndVisualRoutine(),
        ]
    )
    routine_manager.exec()
