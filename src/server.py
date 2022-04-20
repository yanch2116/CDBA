import socket
import json
import threading
import numpy as np

global mode
mode = 1  # 0 stands for no insert keyframe,1 stands for insert keyframe

def getData():
    # Replace Your Own npz File PATH
    npz_path = '../demo/results.npz'
    a = np.load(
        npz_path, allow_pickle=True)['results'][()]
    data = []
    for key in a:
        # temp = np.append(a[key][0]['poses'], a[key][0]['trans'])
        temp = np.append(a[key][0]['poses'], [0,0,0])
        data.append(temp)
    data = list(data)
    for i in range(len(data)):
        data[i] = list(data[i])
    return data  # [N,75]  N stands for the number of frames


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    data = getData()
    num_frame = len(data)
    for frame in range(num_frame):
        d = sock.recv(1024)
        if not d:
            break
        poses = data[frame][:72]
        trans = data[frame][72:75]
        # The data is [mode,poses,trans,current_frame]
        send_data = json.dumps([mode, poses, trans, frame+1]).encode('utf-8')
        print('The current frame is {}'.format(frame+1))
        sock.send(send_data)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(1)
print('Waiting for connection...')

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
