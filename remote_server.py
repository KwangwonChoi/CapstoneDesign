import threading
from socket import *
import numpy as np
import cv2
import time

def get_thermal() :
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
        for i in range(0, 60) :
            for j in range(0, 80) :
	            image[i][j] = data[i * 80 + j]

        cv2.imwrite('test.png', image)
        print("get thermal success")

        waiting_second(2)

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
