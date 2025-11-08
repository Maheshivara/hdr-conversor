import cv2 as cv


class HDRReader:
    def read(self, filepath: str):
        return cv.imread(filepath, cv.IMREAD_UNCHANGED)
