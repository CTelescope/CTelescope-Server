from datetime import datetime
from time import sleep, perf_counter
from os import path, makedirs
from threading import Thread

import cv2

ABS_DIRECTORY = path.dirname(path.realpath(__file__))
URI = "http://192.168.1.30:8080/?action=stream"

record_status = False

def Rafale(Duree, FPS) -> None:
    cap = cv2.VideoCapture(URI)
    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    frame_path = path.join(ABS_DIRECTORY, "gallery/rafales/" + d)
    
    if not path.exists(frame_path):
        makedirs(frame_path)

    for s in range(0,Duree):
        for c in range(0,FPS):
            timer = perf_counter()
            
            frame = cap.read()[1]
            cv2.imwrite(path.join(frame_path, f"{s}-{c}.png"), frame)

            end_time = (1/FPS) - (perf_counter() - timer)
            if end_time > 0 : sleep(end_time)

    cap.release()

def Enregistrement(Duree, FPS) -> None:
    cap = cv2.VideoCapture(URI)

    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    record_path = path.join(ABS_DIRECTORY, "gallery/enregistrements/")

    if not path.exists(record_path):
        makedirs(record_path)
    
    frames = []        
    for _ in range(0,Duree):
        for _ in range(0,FPS):
            timer = perf_counter()
            
            frame = cap.read()[1]
            frames.append(frame)

            end_time = (1/FPS) - (perf_counter() - timer)
            if end_time > 0 : sleep(end_time)
    cap.release()

    height, width, layers = frame.shape
    out = cv2.VideoWriter(path.join(record_path, d + '.avi'), 
                          cv2.VideoWriter_fourcc(*'DIVX'), 
                          FPS, (width,height))
    for f in range(len(frames)):
        out.write(frames[f])
    out.release()

def Capture() -> None:
    cap = cv2.VideoCapture(URI)

    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    capture_path = path.join(ABS_DIRECTORY, "gallery/captures/")

    if not path.exists(capture_path):
        makedirs(capture_path)

    frame = cap.read()[1]
    cv2.imwrite(path.join(capture_path,d + '.png'), frame)

    cap.release()

def StartRecord(FPS) -> None:
    global record_status

    if record_status is False:
        record_status = True
        x = Thread(target=_Record, args=(FPS,))
        x.start()

def StopRecord() -> None:
    global record_status

    if record_status is True:
        record_status = False

def _Record(FPS) -> None:
    global record_status

    cap = cv2.VideoCapture(URI)

    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    record_path = path.join(ABS_DIRECTORY, "gallery/enregistrements/")

    if not path.exists(record_path):
        makedirs(record_path)

    print('[*] Capture des images')

    frames = []

    while record_status:
        for _ in range(0,FPS):
            timer = perf_counter()
            
            frame = cap.read()[1]
            frames.append(frame)

            end_time = (1/FPS) - (perf_counter() - timer)
            if end_time > 0 : sleep(end_time)
    cap.release()

    print('[*] Ecriture de la video')

    height, width, layers = frame.shape
    out = cv2.VideoWriter(path.join(record_path, d + '.avi'), 
                          cv2.VideoWriter_fourcc(*'DIVX'), 
                          FPS, (width,height))

    for f in range(len(frames)):
        out.write(frames[f])
        print(f"write : {f}", end='\r')
    out.release()

if __name__ == '__main__':
    StartRecord(24)
    sleep(15)
    StopRecord()
    print('\n')