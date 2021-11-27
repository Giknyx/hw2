import socket
from _thread import start_new_thread

host = 'localhost'
port = 5555

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientsocket.connect((host, port))
except socket.error as e:
    print(e)


def read_response():
    while True:
        response = clientsocket.recv(1024)
        if response.decode("utf-8") == "/partner_left":
            print("Your partner left, use '/exit' to leave the chat")
            clientsocket.send(str.encode("/partner_left"))
            break
        print(response.decode('utf-8'))


start_new_thread(read_response, ())
while True:
    message = input()
    if not message:
        continue        # for some reason when server recv b'' it raises an exception
    clientsocket.send(str.encode(message))
    if message == "/exit":
        break

clientsocket.close()
