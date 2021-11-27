import socket
from _thread import start_new_thread

host = '127.0.0.1'
port = 5555
thread_count = 0
rooms = [[]]    # they will be changing constantly

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(100)

print('Server is running. Press ctrl+c to stop')
print('Listening for connections')


def client_talk(connection, room_num, partner_num):
    connection.send(str.encode('Connection started! To leave the chat use "/exit".'))
    connection.send(str.encode('Waiting for your partner...'))

    while len(rooms[room_num]) < 2:
        continue

    connection.send(str.encode('Your partner has joined the chat!'))

    while True:
        data = connection.recv(1024)        # for some reason it raises an exception when recv b''
        if not data or data.decode("utf-8") == "/exit":
            rooms[room_num][partner_num].send(str.encode("/partner_left"))
            break
        if data.decode("utf-8") == "/partner_left":
            rooms[room_num].clear()         # clearing the room for future users
            while True:                     # waiting for the remaining user in room to leave
                data = connection.recv(1024)
                if not data or data.decode("utf-8") == "/exit":
                    break
            break
        rooms[room_num][partner_num].send(data)

    connection.close()


while True:
    conn, address = serversocket.accept()
    print(f'New connection established: {address}')

    # Looking for an empty space for the new user
    room_num = -1
    partner_num = 1
    for i in range(len(rooms)):
        if len(rooms[i]) == 0:
            partner_num = 1
            room_num = i
            break
        elif len(rooms[i]) == 1:
            partner_num = 0
            room_num = i
            break
    if room_num == -1:
        rooms.append([])
        room_num == len(rooms) - 1
        partner_num = 1
    rooms[room_num].append(conn)
    start_new_thread(client_talk, (conn, room_num, partner_num, ))
    thread_count += 1
    print(f'Thread number: {thread_count}')
