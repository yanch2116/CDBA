import socket
import json
import threading
import pickle

global mode
mode = 0  # 0 stands for not inserting the frame,1 stands for inserting the frame


def getData():
    path = '/Users/yanch/Downloads/results.pkl'
    f = open(path, 'rb')
    data = pickle.load(f)['pred_numpy_save'][0]
    data = list(data)
    for i in range(len(data)):
        data[i] = list(data[i])
    return data


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send('Connect Succeed!')
    data = getData()
    num_frame = len(data)
    for frame in range(num_frame):
        d = sock.recv(1024)
        if not d:
            break
        poses = data[frame][:72]
        trans = data[frame][72:75]
        send_data = json.dumps([mode, poses, trans, frame+1]).encode('utf-8')
        print('The current frame is {}'.format(frame+1))
        # send_data = json.dumps([mode, json.dumps(poses), json.dumps(trans), frame+1])
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
