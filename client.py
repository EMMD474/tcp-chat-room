import socket
import threading as t

nick = input('Choose a nickname: ')

#creating a socket and connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5050))

#a function that receives msgs from the server
def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "NICK":
                client.send(nick.encode('ascii'))
            else:
                print(msg)
        except:
            print('an Error occurred!')
            client.close()
            break

def write():
    while True:
        msg = f"[{nick}]: {input('')}"
        client.send(msg.encode('ascii'))

r_thread = t.Thread(target=receive)
r_thread.start()

w_thread = t.Thread(target=write)
w_thread.start()
