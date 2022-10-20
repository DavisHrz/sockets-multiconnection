import threading as th
import sys
import socket
import selectors
import types

host = '192.168.100.152'  # Localhost
port = 65432        # Port to listen on (non-privileged ports are > 1023)
list_client = {}    # List of clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_server():
    try:
        server.bind((host, port))
        server.listen()
        print('Server on', (host, port))

        while True:
            conn, addr = server.accept()
            add_client(conn, addr)
    except:
        print('Server closed')

def add_client(client, addr):
    uid = str(addr[0])+":"+str(len(list_client))
    hilo_esuccha = th.Thread(target=listener_mesagges, args=(client, uid))

    list_client[uid] = {
        'client': client, 
        'addr': addr,
        'hilo_esuccha': hilo_esuccha,
    }
    
    hilo_esuccha.start()

    print('Connected by', addr, 'uid:', uid)
    send_message(client, 'Bienvenido al server!')

def listener_mesagges(client, uid):
    try:
        while True:
            message = client.recv(1024)
            if message.decode('utf-8') == 'salir':
                disconnect_client(uid)
                break
            else:
                print(message.decode('utf-8'))
    except:
        disconnect_client(uid)

def send_message(client, message):
    msg = str(message).encode('utf-8')
    client.send(msg)

def disconnect_client(uid):
    list_client[uid]['client'].close()
    del list_client[uid]
    print('Client disconnected: ', uid)

def disconnect_server():
    server.close()

def say_hello():
    for uid in list_client:
        print('Sending hello to', uid)
        send_message(list_client[uid]['client'], 'Hola '+ uid + ' !') 

def main():
    start_server()

if __name__ == '__main__':
    main()

