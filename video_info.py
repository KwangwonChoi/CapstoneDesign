import cv2
import numpy as np

address = "rtsp://20.20.1.247:8160"


class video_info:
    def __init__(self):
        self.video = cv2.VideoCapture(address)

    def get_frame(self):
        _, frame = self.video.read()
        return frame
