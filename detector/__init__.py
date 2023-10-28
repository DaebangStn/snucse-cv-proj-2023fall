from .harris import Harris
from .hough_line import HoughLine


detectors = {
    'harris': Harris,
    'hough': HoughLine,
}