import csv
import math
import pickle
from typing import List

import numpy as np

from routines.constants import Context
from utils.timing import UET


class PersonRepresentation:
    """
    Sometimes we need to combine multiple features across 4 cameras
    Be it direct coordinates for multi-view, or pseudo multi-view I am using here.
    It does necessarily mean that some data is lost.
    For this particular class angle metrics are selected either closest to 0 or closest to pi / 2
    If you want to change anything about multi-view, first go to Person class, afterward ammend this class.
    """
    def __init__(
            self,
            tag: str,
            context: Context
    ):
        self.representations = [
            self.__read_representation_file(
                context.PRIMARY_FEATURE_VECTORS_PER_VIDEO_PATH + f"{video_id}/" + f"{tag}.emb"
            ) for video_id in range(context.NUMBER_OF_VIDEOS)
        ]
        self.uets = [
            self.__read_representation_file(
                context.UET_ROOT_FOLDER + f"{video_id}.uets"
            ) for video_id in range(context.NUMBER_OF_VIDEOS)
        ]
        self.__context = context
        self.window_us = context.MOVEMENT_OBSERVATION_WINDOW_SECONDS * 10 ** 6

        self.__body_part_mapping = dict(
                x=0,
                y=1,
                bbwh=2,
                ang_left_arm=3,
                ang_right_arm=4,
                ang_neck_back=5,
                ang_eye_shoulder=6,
                left_arm_ratio=7,
                right_arm_ratio=8
        )


    def __find_uet(self, uet_list: List[UET], uet: UET) -> int:
        left = 0
        right = len(uet_list) - 1

        if uet_list[-1] < uet:
            return None

        if uet_list[left] > uet:
            return None

        while right - left > 1:
            mid = (left + right) // 2
            if uet_list[mid] > uet:
                right = mid
            elif uet_list[mid] < uet:
                left = mid
            else:
                return mid

        if abs(uet_list[left] - uet) < abs(uet_list[right] - uet):
            return left
        else:
            return right

    def __find_representations_by_uet(self, uet: UET):
        indexes = list(map(
            self.__find_uet, self.uets, [uet] * 4
        ))
        return indexes

    def __restricted(
            self,
            index: int,
            video_index: int
    ):
        return index < self.__context.TIMESTAMP_CUTOFF_FRAMES[video_index]

    def produce_feature_vectors(self, uet_space: List[UET]):
        """
        Well, this is a bunch of spaghetti shit I don't wanna refactor
        :param uet_space:
        :return:
        """
        feature_vectors = []
        for uet in uet_space:
            feature_vectors.append([uet])
            embedding_indexes = self.__find_representations_by_uet(uet)
            embeddings = []

            participating_cameras = set()

            for i in range(len(self.representations)):
                if embedding_indexes[i] is not None:
                    if not self.__restricted(embedding_indexes[i], i):
                        to_float = lambda x: None if x == '' else float(x)
                        embeddings.append(list(map(to_float, self.representations[i][embedding_indexes[i]])))
                        participating_cameras.add(i)

            embeddings = np.array(embeddings).T


            VARIATIVITY = len(embeddings[0])

            # arm criteria is that the ratio is closest to 1
            distance_to_1 = lambda x: abs(1 - x)

            #Angle left arm-elb
            selected_aLE = embeddings[
                self.__body_part_mapping['ang_left_arm']
            ][0]
            current_minimum = 20000
            for i in range(VARIATIVITY):
                if embeddings[self.__body_part_mapping['left_arm_ratio']][i] is not None:
                    if distance_to_1(embeddings[self.__body_part_mapping['left_arm_ratio']][i]) < current_minimum:
                        selected_aLE = embeddings[self.__body_part_mapping['ang_left_arm']][i]

            feature_vectors[-1].append(selected_aLE)
            #Angle right arm-elb
            selected_aRE = embeddings[self.__body_part_mapping['ang_right_arm']][0]
            current_minimum = 20000
            for i in range(VARIATIVITY):
                if embeddings[self.__body_part_mapping['right_arm_ratio']][i] is not None:
                    if distance_to_1(embeddings[self.__body_part_mapping['right_arm_ratio']][i]) < current_minimum:
                        selected_aRE = embeddings[self.__body_part_mapping['ang_right_arm']][i]

            feature_vectors[-1].append(selected_aRE)
            #]Angle eye-shoulder
            angSE = min(abs(math.pi / 2 - emb) if emb is not None else 100 for emb in embeddings[self.__body_part_mapping['ang_eye_shoulder']])
            feature_vectors[-1].append(angSE)
            #Angle neck-back
            angNB = min(abs(math.pi / 2 - emb) if emb is not None else -100 for emb in embeddings[self.__body_part_mapping['ang_neck_back']])
            feature_vectors[-1].append(angNB)
            #bbwh
            bbwh = min(emb if emb is not None else -100 for emb in embeddings[self.__body_part_mapping['bbwh']])
            feature_vectors[-1].append(bbwh)
            #Distance covered in last 10 s
            covered_areas = []
            # okay, let's get minimal UET
            for representation_id in participating_cameras:
                X, Y = [], []
                uet_id = self.__find_uet(self.uets[representation_id], uet - self.window_us)
                if uet_id is None:
                    uet_id = 0
                for i in range(uet_id, embedding_indexes[representation_id] + 1):
                    X.append(float(self.representations[representation_id][i][0]))
                    Y.append(float(self.representations[representation_id][i][1]))

                covered_area = (max(X) - min(X)) * (max(Y) - min(Y))
                covered_areas.append(covered_area)

            avg = lambda x: sum(x) / len(x)
            movEMB = avg(covered_areas) / (720 * 1280)
            feature_vectors[-1].append(movEMB)
        return feature_vectors

    def __read_representation_file(self, filename):
        with open(filename, "rb") as f:
            representations = pickle.load(f)
        return representations
