from datetime import datetime
from time import sleep, perf_counter
from os import path, makedirs
from threading import Thread

import cv2

from libraries.logger import setup_logger

logger = setup_logger(__file__)

ABS_DIRECTORY = path.dirname(path.realpath(__file__) ) + "/../"
# URI = "http://0.0.0.0:8080/?action=stream"
URI = "http://150.214.222.102/mjpg/video.mjpg?camera=1"
print(ABS_DIRECTORY)
record_status = False

def Rafale(Duree, FPS):
    global record_status

    if record_status is False:
        record_status = True

        cap = cv2.VideoCapture(URI)
        d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        frame_path = path.join(ABS_DIRECTORY, "gallery/rafales/" + d)

        if not path.exists(frame_path):
            makedirs(frame_path)

        logger.info(f"Start burst : duree {Duree}, FPS {FPS}, Path{frame_path}")

        for s in range(0,Duree):
            for c in range(0,FPS):
                timer = perf_counter()

                frame = cap.read()[1]
                cv2.imwrite(path.join(frame_path, f"{s}-{c}.png"), frame)

                end_time = (1/FPS) - (perf_counter() - timer)
                if end_time > 0 : sleep(end_time)
        
        logger.success(f"Burst done : {frame_path}")

        cap.release()
        
        record_status = False

def Enregistrement(Duree, FPS):
    global record_status

    if record_status is False:
        record_status = True
    
        cap = cv2.VideoCapture(URI)

        d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        record_path = path.join(ABS_DIRECTORY, "gallery/enregistrements/")

        if not path.exists(record_path):
            makedirs(record_path)

        logger.info(f"Debut rec : duree {Duree}, FPS {FPS}, Path{record_path}")
        
        frames = []        
        for _ in range(0,Duree):
            for _ in range(0,FPS):
                timer = perf_counter()

                frame = cap.read()[1]
                frames.append(frame)

                end_time = (1/FPS) - (perf_counter() - timer)
                if end_time > 0 : sleep(end_time)
        cap.release()

        record_status = False

        height, width, layers = frame.shape
        out = cv2.VideoWriter(path.join(record_path, d + '.avi'), 
                              cv2.VideoWriter_fourcc(*'DIVX'), 
                              FPS, (width,height))
        for f in range(len(frames)):
            out.write(frames[f])
            logger.status(f"write : {f}")

        logger.success(f"Rec done : {frame_path}")

        out.release()

def Capture():
    global record_status

    if record_status is False:
        record_status = True

        cap = cv2.VideoCapture(URI)

        d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        capture_path = path.join(ABS_DIRECTORY, "gallery/captures/")

        logger.info(f"New capture {capture_path}")

        if not path.exists(capture_path):
            makedirs(capture_path)

        frame = cap.read()[1]
        cv2.imwrite(path.join(capture_path,d + '.png'), frame)

        cap.release()

        record_status = False

def StartRecord(FPS):
    global record_status

    if record_status is False:
        record_status = True
        record = Thread(target=_Record, args=(FPS,))
        record.start()

def StopRecord():
    global record_status

    if record_status is True:
        record_status = False

def _Record(FPS):
    global record_status

    cap = cv2.VideoCapture(URI)

    d = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    record_path = path.join(ABS_DIRECTORY, "gallery/enregistrements/")

    if not path.exists(record_path):
        makedirs(record_path)

    logger.info(f'Record {record_path}')

    frames = []

    while record_status:
        for _ in range(0,FPS):
            timer = perf_counter()
            
            frame = cap.read()[1]
            frames.append(frame)

            end_time = (1/FPS) - (perf_counter() - timer)
            if end_time > 0 : sleep(end_time)
    
    cap.release()

    logger.info('Ecriture de la video')

    height, width, layers = frame.shape
    out = cv2.VideoWriter(path.join(record_path, d + '.avi'), 
                          cv2.VideoWriter_fourcc(*'DIVX'), 
                          FPS, (width,height))

    for f in range(len(frames)):
        out.write(frames[f])
        logger.status(f"write : {f}")
    out.release()

if __name__ == '__main__':
    StartRecord(24)
    sleep(15)
    StopRecord()
    print('\n')