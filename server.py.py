import socket
import threading as t

host = '127.0.0.1'
port = 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(msg):
    for client in clients: 
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick = nicknames[index]
            broadcast(f"{nick} has left the chat!".encode('ascii'))
            print(f'{nick} has the the chat!')
            nicknames.remove(nick)
            break


def receive():
    while True:
        client, addr = server.accept()
        print(f"[{addr}] has connected to server!")

        client.send('NICK'.encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        nicknames.append(nick)
        clients.append(client)

        print(f'Nick name of client is {nick}')
        client.send('Connection to server successful!'.encode('ascii'))
        broadcast(f"[ALERT]: {nick} has joined the chat!".encode('ascii'))

        thread = t.Thread(target=handle, args=(client,))
        thread.start()

print(F'[LISTENING] Server is listening on {host}')
receive()