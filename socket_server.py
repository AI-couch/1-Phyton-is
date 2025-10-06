# import  socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('192.168.100.245', 8888))
# s.listen(1)
# conn, addr = s.accept()
# while True:
#     data1 = conn.recv(1024)
#     data2 = (b"Hello from server")
#     if not data1: break
#     conn.sendall(data2)
#     print(data1)
# conn.close()



import  socket
HOST = "192.168.164.178"  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
# Create an INET, STREAMing socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
    serv_sock.bind((HOST, PORT))
    serv_sock.listen(1)
    print("\n\nСервер сокета запущен. Ждем подключения клиента")
    sock, addr = serv_sock.accept()
    with sock:
        print("Подключен клиент ", addr)
        print("Ожидай сообщения от клиента")
        while True:
            # Receive
            data_bytes = sock.recv(1024)
            data = data_bytes.decode()
            print(f"\nОт хоста {addr} получены данные:\n", repr(data))
            if not data:
                break
            # Process
            if data == b"close":
                print(f'ты разорвал соединение\n')
                break
            # data = data.upper()
            inp =input("напиши ответ: ")
            if inp == 'close':
                break
            inpBytes=inp.encode()
            # Send
            sock.sendall(inpBytes)
            print(f"Ответ отправлен хосту {addr}\n ждем новое сообщение от клиента")

        print("Сокет ликвидирован", addr)
        # sock.close()  # No need as wrapped with "with sock:"








# ##веб сокет сервер 

# import asyncio
# from websockets.server import serve

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)

# async def main():
#     async with serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever

# asyncio.run(main())