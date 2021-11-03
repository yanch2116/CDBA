import cv2
import json
import socket
import numpy as np
from io import BytesIO
import struct


# Capture frame
cap = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9998))

while cap.isOpened():
    _, frame = cap.read()
    dim = (128, 128)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    print(frame[0][0])
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

    memfile = BytesIO()
    np.save(memfile, frame)
    memfile.seek(0)
    data = memfile.read()

    s.sendall(struct.pack("L", len(data)) + data)

cap.release()
