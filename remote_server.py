import threading
from socket import *
import numpy as np
import cv2
import time
import face_harr2 as harr

def get_thermal() :
    count = 0
    while True :
        thermalSock = socket(AF_INET, SOCK_STREAM)
        thermalSock.connect(('20.20.1.4', 8080))
        data = np.array([], dtype="uint8")
        while True :
            temp = thermalSock.recv(1024)
            temp = np.fromstring(temp, 'uint8')
            data = np.append(data, temp)
            if len(data) >= 4800 :
                break

        image = np.ndarray(shape=(60, 80), dtype='uint8')
        
        for i in range(0, 60):
            for j in range(0, 80):
                image[i][j] = data[i * 80 + j]

        image = cv2.resize(image, (320, 240), interpolation=cv2.INTER_LINEAR)

        name = "./photos/tst" + str(count) + ".png"
        count += 1
        cv2.imwrite(name, image)

        bbox = harr.detection_face_harr(image)

        if len(bbox) == 0 :
            print("failure to detection!")
            waiting_second(2)
        else:
            print("success to detecton!")
            print(bbox)
            waiting_second(3)

def motion_detect() :
    motionSock = socket(AF_INET, SOCK_STREAM)
    motionSock.connect(('20.20.1.4', 8081))
    while True :
        data = (motionSock.recv(1024)).decode('utf-8')

        if data == "true" :
            print("모션감지!! ", data)
        waiting_second(2)

def waiting_second(second) :
    for i in range(0, second) :
        print(i+1, '초 대기중...')
        time.sleep(1)

print("thread start")

thermal_t = threading.Thread(target=get_thermal, args=())
motion_t = threading.Thread(target=motion_detect, args=())

motion_t.start()
thermal_t.start()
