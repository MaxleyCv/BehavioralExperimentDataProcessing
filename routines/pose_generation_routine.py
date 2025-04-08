import pickle
from typing import Optional

import torch
from ultralytics import YOLO

from dependencies.dependency_manager import DependencyManager
from dependencies.videos_present_dependency import VideosPresentDependency
from routines.constants import Context
from routines.dependency_reliant_routine import DependencyReliantRoutineMixin, dependency_reliant_method
from routines.routine import Routine
from utils.command_line_interface import CommandInterface


class PoseGenerationRoutine(Routine, DependencyReliantRoutineMixin):
    """
    Using Yolov11-pose provide skeleton and bounding box representations to each frame of the videos.
    """
    def __init__(self):
        context = Context()

        # DEPENDENCIES
        super(DependencyReliantRoutineMixin).__init__(
            DependencyManager(
                dependency_list=[
                    VideosPresentDependency
                ],
                current_routine=self
            )
        )

        self.__number_of_videos = context.NUMBER_OF_VIDEOS
        self.__context = context
        self.__video_paths = [
            context.VIDEO_ROOT_FOLDER + f"{video_id}.mp4"
            for video_id
            in range(self.__number_of_videos)
        ]
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = YOLO('yolo11x-pose.pt')
        # well.... no graphic card and you're stuck here forever
        model.to(device)
        self.__model = model
        self.__interface: Optional[CommandInterface] = None

    @dependency_reliant_method
    def execute(self) -> bool:
        self.__interface = CommandInterface("Starting pose generation routine!")
        status = True
        for video_index in range(self.__number_of_videos):
            status = status and self.__track_model_per_video(self.__video_paths[video_index], video_index)
        return True

    def __track_model_per_video(self, video_path: str, video_id: int) -> bool:
        self.__interface.write_instruction(f"Starting pose generation for {video_path}")
        tracked = self.__model.track(
            source=video_path,
            show=False,
            save=False,
            stream=True
        )

        saved_poses = []

        for prediction in tracked:
            boxes = prediction.boxes.xywh.cpu().tolist()
            skeletons = prediction.keypoints.xy.cpu().tolist()
            if prediction.boxes.id is None:
                ids = []
            else:
                ids = prediction.boxes.id.cpu().tolist()
            saved_poses.append([boxes, skeletons, ids])

        with open(f'{self.__context.POSE_ROOT_FOLDER}vid-{video_id}.poses', 'wb') as f:
            pickle.dump(saved_poses, f)

        return True
