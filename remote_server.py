import threading
from socket import *
import numpy as np
import cv2
import face_harr2 as harr
import firebase_supporter as firebase
import ctypes  # An included library with Python install.
import tkinter
import json
from time import sleep

def get_thermal():
    count = 0


    while True:
        thermalSock = socket(AF_INET, SOCK_STREAM)
        thermalSock.connect(('20.20.1.4', 8080))

        data = []

        length = thermalSock.recv(5)
        length = int(json.loads(length))

        while True:
            temp = thermalSock.recv(1024)
            data += temp

            if len(data) >= length:
                break

        data = json.loads(bytearray(data).decode("utf-8"))

        np_data = np.array(data,np.uint16)
        np_data = np.right_shift(np_data,8,np_data)
        np_data = np.asarray(np_data, dtype=np.uint8)

        image = np_data.reshape((60,80))

        name = "tst" + str(count) + ".png"
        count += 1
        cv2.imwrite(name, image)

        bbox = harr.detection_face_harr(image)

        if len(bbox) == 0:
            print("failure to detection!")
            sleep(2)

        else:
            for b in bbox:
                isValidRect, curThermal = calculate_thermal(data, b)

                if isValidRect:
                    print("success to detecton!")

                    if abs(curThermal - 36.5) > 2:
                        fb.alertRegistration("KwangwonChoi","alert","danger")
                    else:
                        fb.alertRegistration("DoyoungKim","normal","정상")

            sleep(2)

def motion_detect():
    motionSock = socket(AF_INET, SOCK_STREAM)
    motionSock.connect(('20.20.1.4', 8081))
    falseCnt = 0
    while True:
        data = (motionSock.recv(1024)).decode('utf-8')
        if data == "true":
            falseCnt = 0

        if falseCnt >= 2000:
            fb.alertRegistration("DoyoungKim","dead","Don't move")
            falseCnt = 0

        falseCnt += 1

        sleep(0.1)


def messageGUI() :

    def messageCallback(message):
        dict = message[1]

        alertMessage = "환자 이름 : " + dict['id']\
                    + "\n제목 :" + dict['title']\
                    + "\n내용 : " + dict['contents']

        ctypes.windll.user32.MessageBoxW(0, alertMessage , "알림", 0)


    def btn() :
        name = totxt.get()
        context = contexttxt.get("1.0", 'end-1c')
        print("보호자 : ", name, "    보낼내용 : ", context)
        fb.alertRegistration(user=name, state="alert", details=context) #details는 GUI에서 받아오도록.

    fb.listenMessage(messageCallback) #쓰레드 돌면서 주기적으로 메세지 확인. 메세지 확인시 messageCallback함수 호출

    window = tkinter.Tk()
    window.title("Capston_Window")
    window.geometry("480x480+100+100")
    window.resizable(False, False)

    tolabel = tkinter.Label(window, text="보호자 : ")
    tolabel.grid(row="0", column="0")
    totxt = tkinter.Entry(window)
    totxt.config(width=50)
    totxt.grid(row="0", column="1")

    contextlabel = tkinter.Label(window, text="보낼 내용 : ")
    contextlabel.grid(row="1", column="0")
    contexttxt = tkinter.Text(window)
    contexttxt.config(width=50, height=10)
    contexttxt.grid(row="1", column="1")

    btn = tkinter.Button(window, text="전송", command=btn)
    btn.grid(row="4", column="1")

    window.mainloop()

def calculate_thermaldata(value):
    return (value - 27315) / 100

def calculate_thermal(data, bbox) :
    x = bbox[0]
    y = bbox[1]
    w = bbox[0] + bbox[2]
    h = bbox[1] + bbox[3]
    totalThermal = 0
    cnt = 0
    isValidRect = True

    for i in range(x, h):
        for j in range(y, w):

            celcius = calculate_thermaldata(data[i][j][0])

            if celcius >= 35 and celcius <= 41:
                totalThermal += celcius
                cnt += 1

    totalThermal = (totalThermal / cnt)

    if ( cnt / w * h ) <= 0.5:
        isValidRect = False

    return isValidRect, totalThermal


fb = firebase.FirebaseSupporter()
print("thread start")
thermal_t = threading.Thread(target=get_thermal, args=())
motion_t = threading.Thread(target=motion_detect, args=())
gui_t = threading.Thread(target=messageGUI, args=())

motion_t.start()
thermal_t.start()
gui_t.start()
