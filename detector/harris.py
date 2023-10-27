import cv2
import numpy as np
from PIL import Image
from detector.base_detector import BaseDetector, FeatureType


class Harris(BaseDetector):
    def __init__(self, image: Image):
        super().__init__(image)
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

    def detect(self, **kwargs):
        """
        :param kwargs:
        :return: list of points (x, y)
        """
        dst = cv2.cornerHarris(self._image, 5, 11, 0.04)
        dst = cv2.dilate(dst, None)
        spot = dst > 0.05 * dst.max()
        coordinates = np.where(spot)
        points = list(zip(coordinates[1], coordinates[0]))
        return points

    def get_type(self) -> FeatureType:
        return FeatureType.POINT
