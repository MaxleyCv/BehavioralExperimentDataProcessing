import copy
import os
import pickle
import random
from collections import deque
from typing import Optional, List, Dict

import numpy as np
import pandas as pd

from dependencies.dependency_manager import DependencyManager
from routines.constants import Context
from routines.dependency_reliant_routine import DependencyReliantRoutineMixin, dependency_reliant_method
from routines.routine import Routine
from utils.command_line_interface import CommandInterface
from visual_tools.trackable import Trackable
from visual_tools.video_assignment import VideoAssigner

#TODO: refactor this file

class TrackableAssignmentRoutine(Routine, DependencyReliantRoutineMixin):
    """
    Since Yolo v11 does not always track the identities perfectly, it often makes sense to assign them.
    Even after cattle method [Trajectory agnostic cattle counting from UAV, Lishchynskyi, Nikolaidis & Cheng, 2024]
    Some identities remain unassigned (for example, )
    """
    def __init__(self):
        super().__init__(
            dependency_manager=DependencyManager(
                dependency_list=[],
                current_routine=self
            )
        )
        self.__context = Context()
        self.__pose_identity_paths = [
            self.__context.POSE_ROOT_FOLDER + f"vid-{i}.poses"
            for i in range(self.__context.NUMBER_OF_VIDEOS)
        ]
        self.__decomposed_video_paths = [
            self.__context.VIDEO_DECOMPOSITION_ROOT_FOLDER + f"{i}"
            for i in range(self.__context.NUMBER_OF_VIDEOS)
        ]

    @dependency_reliant_method
    def execute(self) -> bool:
        for video_id in range(self.__context.NUMBER_OF_VIDEOS):
            video_folder = self.__context.PRIMARY_FEATURE_VECTORS_PER_VIDEO_PATH + f"{video_id}/"

            if not os.path.exists(video_folder):
                os.makedirs(video_folder)

            primary_trackables = self.__produce_trackables_by_video(
                video_id=video_id,
                identities_path=self.__pose_identity_paths[video_id]
            )
            individualized_data = self.__assign_trackables_their_identities(
                trackables=primary_trackables,
                decomposed_video_path=self.__decomposed_video_paths[video_id]
            )
            selected_feature_vector_dict = self.__select_features_per_instance(
                individualized_data
            )

            for key in selected_feature_vector_dict:
                with open(video_folder + f"{key}.emb", 'wb') as f:
                    pickle.dump(selected_feature_vector_dict[key], f)

        return True

    def __select_features_per_instance(
            self,
            trackable_dict: Dict[str, List[Trackable]]
    ) -> Dict[str, List[List[float | None | int]]]:
        feature_vectors_per_identity = dict()
        for key in self.__context.keys:
            trackables = trackable_dict[key]
            feature_vectors = [t.feature_vectors for t in trackables]
            selected_features = []
            if len(feature_vectors) == 0:
                print(key)
                print(trackable_dict)
            for time_row in range(len(feature_vectors[0])):
                potential_embeddings = [
                    feature_vectors[instance_id][time_row] for instance_id in range(len(feature_vectors))
                ]
                number_of_nones = lambda x: sum(1 if p is None else 0 for p in x)
                potential_embeddings.sort(key=number_of_nones)
                row = potential_embeddings[0]
                selected_features.append(row)
            feature_vectors_per_identity[key] = selected_features
        return feature_vectors_per_identity

    def __produce_last_seen_trackable(self, trackables: List[Trackable]) -> np.array:
        """
        We need to know which trackable is seen when. This is strictly per one video.
        :param trackables:
        :return:
        """
        df = pd.DataFrame({"firstFound": [], "lastFound": [], "length": [], "detectedIDs": [], "indexes": []})

        counter = 0

        for q in range(len(trackables)):
            t = trackables[q]
            first_found = len(t.feature_vectors)
            last_found = 0
            detected_ids = set()
            for i in range(len(t.feature_vectors)):
                if any(t.feature_vectors[i]):
                    first_found = min(first_found, i)
                    last_found = max(last_found, i)
                    detected_ids.add(i)
            df.loc[counter] = [first_found, last_found, len(detected_ids), detected_ids, t.index]
            counter += 1

        return df["lastFound"].to_numpy()

    def __assign_trackables_their_identities(
            self,
            trackables: List[Trackable],
            decomposed_video_path: str
    ) -> Dict[str, List[Trackable]]:
        """
        Produces assignment data for the observed trackables through interaction with the image.
        :param trackables: List of previously produced trackables that need to be merged.
        :param decomposed_video_path: Path do a decomposed video.
        :return: trackables by identity
        """
        trackables_last_found = self.__produce_last_seen_trackable(trackables)
        video_assigner = VideoAssigner(decomposed_video_path)
        for trackable, last_found in zip(trackables, trackables_last_found):
            video_assigner.show_skeleton(last_found, trackable)
        return video_assigner.assignment_data

    def __produce_trackables_by_video(
            self, identities_path: str, video_id: int
    ) -> List[Trackable]:
        interface = CommandInterface(f"Assigning trackable identities to video {video_id}")
        interface.write_instruction(f"Now please use your manifest {self.__context.ip_to_trackable_mapping}")
        interface.write_instruction(f"Use keyboard inputs for the keys")

        transformation_path = self.__context.HOMOGRAPHY_ROOT_FOLDER + f"{video_id}.homography"
        with open(transformation_path, 'rb') as f:
            transformation = pickle.load(f)
        with open(identities_path, 'rb') as f:
            pose_information = pickle.load(f)

        return self.__produce_primary_trackables(transformation, pose_information)

    def __produce_primary_trackables(self, transformation: np.array, pose_information: np.array) -> List[Trackable]:
        iteration = -1

        extra_indexes = deque()
        for i in range(1000, 1500):
            extra_indexes.append(i)

        trackables = []

        for boxes, skeletons, ids in pose_information:
            iteration += 1
            indexes_not_assigned = set(i for i in range(len(boxes)))
            trackables_not_assigned = set(i for i in range(len(trackables)))
            if len(trackables) == 0:
                for i in range(len(ids)):
                    new_trackable = Trackable(
                        boxes[i],
                        skeletons[i],
                        transformation,
                        set_index=int(ids[i])
                    )
                    trackables.append(new_trackable)
                    indexes_not_assigned.remove(i)
                continue
            if len(indexes_not_assigned):
                for idx in copy.copy(indexes_not_assigned):
                    for j in range(len(trackables)):
                        try:
                            if trackables[j].index == int(ids[idx]):
                                trackables[j].feed(boxes[idx], skeletons[idx])
                                trackables_not_assigned.remove(j)
                                indexes_not_assigned.remove(idx)
                        except IndexError:
                            ids.append(extra_indexes.popleft())

                if len(indexes_not_assigned):
                    # Add new trackables
                    for index in copy.copy(indexes_not_assigned):
                        new_trackable = Trackable(
                            boxes[index],
                            skeletons[index],
                            transformation,
                            set_index=int(ids[index]),
                            feed_blanks=True,
                            feed_number=iteration
                        )
                        trackables.append(new_trackable)
                        indexes_not_assigned.remove(index)

            if len(trackables_not_assigned):
                for idx in trackables_not_assigned:
                    trackables[idx].feed_blank()
        return trackables
