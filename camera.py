from time import sleep
import cv2
from datetime import datetime
from os import path
import os

ABS_DIRECTORY = path.dirname(path.realpath(__file__))

cap = cv2.VideoCapture('http://192.168.1.30:8080/?action=stream')

def Rafale(Duree = 5, FPS = 24):
    count = 0
    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    ABSOLUTE_FRAME_PATH = path.join(ABS_DIRECTORY, "Rafales/" + d)
    
    if not os.path.exists(ABSOLUTE_FRAME_PATH):
        os.makedirs(ABSOLUTE_FRAME_PATH)

    for t in range(0,Duree):
        print("sec : ", str(t+1))
        for i in range(0,FPS):
            frame = cap.read()[1]
            cv2.imwrite(path.join(ABSOLUTE_FRAME_PATH, f"{t}-{i}.png"), frame)
            sleep(1/FPS)    
    cap.release()

        

def Enregistrement(duree_record, fps_record):
    count = 0
    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    ABSOLUTE_RECORD_PATH = path.join(ABS_DIRECTORY, "/Enregistrements/")

    if not os.path.exists(ABSOLUTE_RECORD_PATH):
        os.makedirs(ABSOLUTE_RECORD_PATH)

    for t in range(0,duree_record):
        print("sec : ", str(t+1))
        tab = []        
        for i in range(0,fps_record):
            frame = cap.read()[1]
            tab.append(frame)
            sleep(1/fps_record) 
    cap.release()

    height, width, layers = frame.shape
    size = (width,height)

    out = cv2.VideoWriter(path.join(ABSOLUTE_RECORD_PATH, d + '.avi'),cv2.VideoWriter_fourcc(*'DIVX'), fps_record, size)
    
    for i in range(len(tab)):
        out.write(tab[i])
    out.release()

# def Capture():
#     ret, frame = cap.read()
#     cv2.imwrite(f + '.png', frame)

if __name__ == '__main__':
    Enregistrement(5,24)
