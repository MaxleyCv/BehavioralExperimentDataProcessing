import math
from typing import Tuple, Optional

import numpy as np

from utils.homography import eucl_dist, dehomogenize_2d, homogenize


class Person:

    FOREARM_TO_BACKBONE_RATIO = 0.5

    def __init__(self, skeleton, transformed=False):
        self.skeleton = skeleton
        self.transformed_skeleton = skeleton
        self.transformed = transformed

        parts = [
            "Nose",
            "Left Eye",
            "Right Eye",
            "Left Ear",
            "Right Ear",
            "Left Shoulder",
            "Right Shoulder",
            "Left Elbow",
            "Right Elbow",
            "Left Wrist",
            "Right Wrist",
            "Left Hip",
            "Right Hip",
            "Left Knee",
            "Right Knee",
            "Left Ankle",
            "Right Ankle"
        ]

        part_key_mapping: dict = dict()

        for i in range(len(parts)):
            part_key_mapping[parts[i]] = i

        self.__PART_KEY_MAPPING = part_key_mapping


    def get_body_part(self, body_part: str, raise_alert: bool = True):
        default_part = self.skeleton[self.__PART_KEY_MAPPING[body_part]]

        check = np.array(default_part)
        if check.dot(check) < 0.1:
            if raise_alert:
                raise ValueError
            else:
                return None

        return default_part

    def planar_view(self):
        try:
            right_shoulder = self.get_body_part('Right Shoulder')
            left_shoulder = self.get_body_part('Left Shoulder')
        except ValueError:
            return False

        ptop, pbottom = self.backbone()

        shoulder_dist = eucl_dist(left_shoulder, right_shoulder)
        backbone_dist = eucl_dist(ptop, pbottom)
        return shoulder_dist >= 0.6 * backbone_dist


    def backbone(self, perspective=False):
        shoulder_right = self.get_body_part('Right Shoulder')
        shoulder_left = self.get_body_part('Left Shoulder')
        hip_right = self.get_body_part('Right Hip')
        hip_left = self.get_body_part('Left Hip')
        shoulder_left, shoulder_right, hip_left, hip_right = map(homogenize, (shoulder_left, shoulder_right, hip_left, hip_right))
        left_line, right_line = np.cross(
            shoulder_left, hip_left
        ), np.cross(
            shoulder_right, hip_right
        )
        diagonals = [
            np.cross(shoulder_right, hip_left),
            np.cross(shoulder_left, hip_right)
        ]

        point_mid = np.cross(*diagonals)
        point_inf = np.cross(left_line, right_line)

        middle_line = np.cross(point_mid, point_inf)

        shoulder_line = np.cross(shoulder_left, shoulder_right)
        hip_line = np.cross(hip_left, hip_right)

        ptop = np.cross(middle_line, shoulder_line)
        pbottom = np.cross(middle_line, hip_line)

        if perspective:
            return ptop, pbottom
        return list(map(int, dehomogenize_2d(ptop))), list(map(int, dehomogenize_2d(pbottom)))

    def left_arm(self, perspective=False):
        wrist = self.get_body_part('Left Wrist')
        elbow = self.get_body_part('Left Elbow')

        if perspective:
            return map(homogenize, (elbow, wrist))
        else:
            return elbow, wrist

    def right_arm(self, perspective=False):
        wrist = self.get_body_part('Right Wrist')
        elbow = self.get_body_part('Right Elbow')

        if perspective:
            return map(homogenize, (elbow, wrist))
        else:
            return elbow, wrist

    def left_arm_dz(self) -> Optional[float]:
        """
        Also not used in any of the feature vectors. But is a depth difference estimator/
        :return:
        """
        try:
            backbone_top, backbone_bottom = self.backbone()
            left_elbow, left_wrist = self.left_arm()
        except ValueError:
            return None

        backbone_distance = eucl_dist(backbone_top, backbone_bottom)
        armdistance = backbone_distance * self.FOREARM_TO_BACKBONE_RATIO
        observed_armdistance = eucl_dist(left_elbow, left_wrist)

        point_to_top = left_elbow[1] < left_wrist[1]

        z2 = armdistance ** 2 - observed_armdistance ** 2

        if z2 <= 0:
            return 0

        return z2

    def shoulder_arm_angle(self, arm_choice: str) -> Tuple[float, float]:
        if arm_choice not in {"Left", "Right"}:
            raise NotImplementedError(
                f"Well, seems like people has not grown {arm_choice} arm. Btw make first letter Uppercase"
            )
        shoulder = np.array(self.get_body_part(f'{arm_choice} Shoulder'))
        elbow = np.array(self.get_body_part(f'{arm_choice} Elbow'))
        wrist = np.array(self.get_body_part(f'{arm_choice} Wrist'))

        observed_ratio = eucl_dist(elbow, shoulder) / eucl_dist(elbow, wrist)

        dx_elbow_wrist, dy_elbow_wrist = wrist - elbow
        dx_elbow_shoulder, dy_elbow_shoulder = wrist - shoulder

        if self.planar_view():
            vect_a = np.array([dx_elbow_shoulder, dy_elbow_shoulder, 0])
            vect_b = np.array([dx_elbow_wrist, dy_elbow_wrist, 0])
        else:
            vect_a = np.array([dx_elbow_shoulder, dy_elbow_shoulder, 0])
            vect_b = np.array([dx_elbow_wrist, dy_elbow_wrist, 0])

        find_angle = lambda a, b: math.acos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

        return find_angle(vect_a, vect_b), observed_ratio

    def right_shoulder_arm_angle(self) -> Tuple[float, float]:
        return self.shoulder_arm_angle("Right")

    def left_shoulder_arm_angle(self) -> Tuple[float, float]:
        return self.shoulder_arm_angle("Left")

    def right_arm_backbone_angle(self) -> float:
        """
        This one is not used in any feature vector but certainly can be expanded upon
        :return:
        """
        try:
            backbone_top, backbone_bottom = self.backbone()
            elbow, wrist = self.right_arm()
        except ValueError:
            return None

        backbone_distance = eucl_dist(backbone_top, backbone_bottom)
        armdistance = backbone_distance * self.FOREARM_TO_BACKBONE_RATIO
        observed_armdistance = eucl_dist(elbow, wrist)

        point_to_top = elbow[1] < wrist[1]

        z2 = armdistance ** 2 - observed_armdistance ** 2
        if z2 <= 0:
            if point_to_top:
                return 0
            # flat person
            return 2 * math.pi
        else:
            z = math.sqrt(z2)
            dy = wrist[1] - elbow[1]
            return math.atan(dy / z) + math.pi / 2

    def eye_shoulder_angle(self):
        left_eye = self.get_body_part('Left Eye')
        right_eye = self.get_body_part('Right Eye')
        left_shoulder = self.get_body_part('Left Shoulder')
        right_shoulder = self.get_body_part('Right Shoulder')

        eyeline = np.array(left_eye) - np.array(right_eye)
        shoulderline = np.array(left_shoulder) - np.array(right_shoulder)

        find_angle = lambda a, b: math.acos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

        return find_angle(eyeline, shoulderline)

    def backbone_neck_angle(self):
        ptop, pbottom = self.backbone()
        nose = self.get_body_part('Nose')
        backbone_vector = np.array(ptop) - np.array(pbottom)
        nose_vector = np.array(ptop) - np.array(nose)
        find_angle = lambda a, b: math.acos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        return find_angle(backbone_vector, nose_vector)
