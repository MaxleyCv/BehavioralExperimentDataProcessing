import csv

import numpy as np

from utils.homography import dehomogenize_2d
from visual_tools.person import Person


class Trackable:
    """
    This is a visual space feature producer class that will allow to process single-view features.
    I am a little bit tired to refactor this, so I put this as my tech debt to this project to the times less dark
    """
    def __init__(
            self, box, skeleton, transform, set_index, feed_blanks=False, feed_number=0
    ):
        self.feature_vectors = []

        if feed_blanks:
            self.feed_n_blanks(feed_number)

        self.index = set_index
        self.box = box
        self.skeleton = skeleton
        self.transform = transform
        self.__perform_measurements()
        self.out_of_sight = False
        self.last_feature_vector = [None for _ in range(9)]

    def centroid_distance(self, another_box):
        x, y, w, h = self.box
        centroid_1 = np.array([x + w / 2, y + h / 2])
        x1, y1, w1, h1 = another_box
        centroid_2 = np.array([x1 + w1 / 2, y1 + h1 / 2])
        return np.linalg.norm(centroid_1 - centroid_2)

    def feed(self, box, skeleton):
        self.box = box
        self.skeleton = skeleton
        self.__perform_measurements()
        return self

    def feed_blank(self):
        self.last_feature_vector = [None for _ in range(9)]
        self.feature_vectors.append(self.last_feature_vector)

    def set_not_detected(self):
        self.out_of_sight = True

    def feed_n_blanks(self, n):
        for _ in range(n):
            self.feed_blank()

    def __perform_measurements(self):
        """
        FEATURE_SET
        :return:
        """
        self.person = Person(self.skeleton)
        try:
            ang_left_arm, left_arm_ratio = self.person.left_shoulder_arm_angle()
        except ValueError as e:
            ang_left_arm, left_arm_ratio = None, None
        try:
            ang_right_arm, right_arm_ratio = self.person.right_shoulder_arm_angle()
        except ValueError as e:
            ang_right_arm, right_arm_ratio = None, None
        try:
            ang_neck_back = self.person.backbone_neck_angle()
        except ValueError as e:
            ang_neck_back = None
        try:
            ang_eye_shoulder = self.person.eye_shoulder_angle()
        except ValueError as e:
            ang_eye_shoulder = None
        bbwh = self.box[2] / self.box[3]

        x, y, w, h = self.box

        X = np.array([x + w / 2, y + h, 1])
        new_x, new_y = dehomogenize_2d(self.transform @ X)
        self.last_feature_vector = [
            new_x,
            new_y,
            bbwh,
            ang_left_arm,
            ang_right_arm,
            ang_neck_back,
            ang_eye_shoulder,
            left_arm_ratio,
            right_arm_ratio
        ]
        self.feature_vectors.append(self.last_feature_vector)
        return self
