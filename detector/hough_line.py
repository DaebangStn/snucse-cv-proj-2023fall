import cv2
import numpy as np
from PIL import Image
from detector.base_detector import BaseDetector, FeatureType


class HoughLine(BaseDetector):
    def __init__(self, image: Image):
        super().__init__(image)
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

    def detect(self, **kwargs):
        """
        Probabilistic Harris Corner Transform
        refer to https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
        :param kwargs:
        :return: list of line end points (x1, y1, x2, y2)
        """
        edges = cv2.Canny(self._image, 50, 200)
        linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, None, 30, 10)
        lines = []
        if linesP is not None:
            for i in range(0, len(linesP)):
                edge = linesP[i][0]
                lines.append((edge[0], edge[1], edge[2], edge[3]))
        return lines

    def get_type(self) -> FeatureType:
        return FeatureType.LINE
