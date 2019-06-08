import struct
from socket import *
import socket
import numpy as np
import cv2
from time import sleep
clntSock = socket.socket(AF_INET, SOCK_STREAM)
clntSock.connect(('20.20.1.4', 8080))
data = np.array([],dtype="uint8")

while True :
	temp = clntSock.recv(1024)
	temp = np.fromstring(temp, 'uint8')
	data = np.append(data, temp)
	if len(data) >= 4800 :
		break

image = np.ndarray(shape=(60, 80), dtype='uint8')
for i in range(0, 60) : 
	for j in range(0, 80) :
		image[i][j] = data[i * 80 + j]

cv2.imwrite('test.png', image)
