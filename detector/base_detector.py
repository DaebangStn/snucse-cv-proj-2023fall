from enum import IntEnum, auto
from abc import abstractmethod
import cv2
import numpy as np
from PIL import Image


class FeatureType(IntEnum):
    POINT = auto()
    LINE = auto()


class BaseDetector:
    def __init__(self, image: Image):
        self._image = self._imagePIL_to_cv2(image)

    @abstractmethod
    def get_type(self) -> FeatureType:
        pass

    @abstractmethod
    def detect(self, **kwargs):
        pass

    @staticmethod
    def _imagePIL_to_cv2(image: Image):
        img_np = np.array(image)
        img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        return img_cv2

