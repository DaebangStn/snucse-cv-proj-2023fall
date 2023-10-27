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
        Harris Corner Detection with SubPixel Accuracy
        refer to https://docs.opencv.org/3.4/dc/d0d/tutorial_py_features_harris.html
        :param kwargs:
        :return: list of points (x, y)
        """
        dst = cv2.cornerHarris(self._image, 5, 11, 0.04)
        dst = cv2.dilate(dst, None)
        ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(self._image, np.float32(centroids), (5, 5), (-1, -1), criteria)
        points = [(int(x), int(y)) for x, y in corners]
        return points

    def get_type(self) -> FeatureType:
        return FeatureType.POINT
