import pickle

import numpy as np
import torch
from ultralytics import YOLO

from routines.constants import Context
from routines.routine import Routine
from utils.command_line_interface import CommandInterface


class PoseGenerationRoutine(Routine):
    """
    Using Yolov11-pose provide skeleton and bounding box representations to each frame of the videos.
    """
    def __init__(self, number_of_videos: int):
        context = Context()
        self.__number_of_videos = number_of_videos
        self.__context = context
        self.__video_paths = [
            context.VIDEO_ROOT_FOLDER + f"{video_id}.mp4"
            for video_id
            in range(number_of_videos)
        ]
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = YOLO('yolo11x-pose.pt')
        # well.... no graphic card and you're stuck here forever
        model.to(device)
        self.__model = model

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
