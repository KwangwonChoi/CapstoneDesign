import video_info
import cv2

video = video_info.video_info()

while(True):
    cv2.imshow("test", video.get_frame())
    cv2.waitKey(1)