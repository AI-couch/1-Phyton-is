import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://192.168.100.245:8765") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()




# import socket 
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('192.168.100.1', 8888))
# s.sendall(b'hello from client')
# data=s.recv(1024)
# s.close()
# print("данные :", repr(data))
