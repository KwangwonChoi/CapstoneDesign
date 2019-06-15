import threading
from socket import *
import numpy as np
import cv2
import time
import face_harr2 as harr

def get_thermal():
    count = 0
    thermalArr = list()

    while True:
        thermalSock = socket(AF_INET, SOCK_STREAM)
        thermalSock.connect(('20.20.1.4', 8080))
        data = np.array([], dtype="uint8")
        while True:
            temp = thermalSock.recv(1024)
            temp = np.frombuffer(temp, 'uint8')
            data = np.append(data, temp)
            if len(data) >= 4800:
                break

        image = np.ndarray(shape=(60, 80), dtype='uint8')

        for i in range(0, 60):
            for j in range(0, 80):
                image[i][j] = data[i * 80 + j]

        image = cv2.resize(image, (320, 240), interpolation=cv2.INTER_LINEAR)

        name = "./thermal_image/tst" + str(count) + ".png"
        count += 1
        cv2.imwrite(name, image)

        bbox = harr.detection_face_harr(image)

        if len(bbox) == 0:
            print("failure to detection!")
            waiting_second(2)
        else:
            print("success to detecton!")
            thermalArr.append(int(calcluate_thermal(image, bbox)))
            if len(thermalArr) > 10 :
                del thermalArr[0]
            check_thermal(thermalArr)
            waiting_second(3)

def motion_detect():
    motionArr = list()
    motionSock = socket(AF_INET, SOCK_STREAM)
    motionSock.connect(('20.20.1.4', 8081))
    while True:
        data = (motionSock.recv(1024)).decode('utf-8')
        if data == "true":
            print("모션감지!! ", data)
        else :
            print("죽었나봐요!!")
        motionArr.append(data)
        if len(motionArr) >= 60 :
            del motionArr[0]
            check_motion(motionArr)
        waiting_second(1)


def waiting_second(second):
    for i in range(0, second):
        print(i + 1, '초 대기중...')
        time.sleep(1)

def calcluate_thermal(image, bbox) :
    x = bbox[0][0]
    y = bbox[0][1]
    w = bbox[0][0] + bbox[0][2]
    h = bbox[0][1] + bbox[0][3]
    totalThermal = 0
    cnt = 0
    for i in range(x, h):
        for j in range(y, w):
            totalThermal += image[i][j]
            cnt += 1

    totalThermal = (totalThermal / cnt) * 255
    return totalThermal

def check_thermal(thermalArr) :
    for i in range(10, 0) :
        print("온도변화폭은 종휘가 알려줄거에요")

def check_motion(motionArr) :
    cnt = 0
    for i in range(60, 0) :
        if(motionArr[i] == "true") :
            return;
    print("1분 동안 움직임이 없어요.. 진짜 죽었나봐요 ㅜㅜ")

print("thread start")
thermal_t = threading.Thread(target=get_thermal, args=())
motion_t = threading.Thread(target=motion_detect, args=())

motion_t.start()
thermal_t.start()
