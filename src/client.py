import socket
import json
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
while True:
    s.send(b'1')
    data = s.recv(4096)
    if data:
        data = json.loads(data.decode('utf-8'))
        print(data[0],data[1][0],data[2][0],data[3])
    else:
        break
s.close()
