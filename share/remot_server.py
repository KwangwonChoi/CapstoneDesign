import threading
from socket import *
import socket
import numpy as np
import cv2
from time import sleep


def get_thermal() : 
    motionSock = socket.socket(AF_INET, SOCK_STREAM)
    motionSock.connect(('20.20.1.4', 8080))

    data = np.array([],dtype="uint8")

    while True : 
        while True :
            temp = clntSock.recv(1024)
            temp = np.fromstring(temp, 'uint8')
            data = np.append(data, temp)
            if len(data) >= 4800 :
                break

        image = np.ndarray(shape=(240, 320), dtype='short')
	for i in range(0, 60) :
    	    for j in range(0, 80) :
                image[i][j] = data[i * 80 + j]

	image = cv2.resize(image, (320, 240), interpolation = cv2.INTER_LINEAR)
        cv2.imwrite('test.png', image)
        print("get thermal success")
        time.sleep(30)

def motion_detect() :
    motionSock = socket.socket(AF_INET, SOCK_STREAM)
    motionSock.connect(('20.20.1.4', 8081))

    while True :
        data = motionSock.recv(1024)
        if data == "true" : 
            print(data)
        else :
            print(data)
        time.sleep(2)

print("thread start") 
thermal_t = threading.Thread(target=get_thermal, args=())
#motion_t = threading.Thread(target=motion_detect, args=())

thermal_t.run()
#motion_t.run()

thermal_t.join()
#motion_t.join()

