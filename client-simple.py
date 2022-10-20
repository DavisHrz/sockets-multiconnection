from pynput import keyboard
import threading as th
import socket

host = '192.168.100.152'  # Localhost
port = 65432        # Port to listen on (non-privileged ports are > 1023)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def on_press(key):
    print('{0} pressed'.format(key))

def received_message(client):
    try:
        while True:
            data = client.recv(1024)
            if data:
                print(data.decode('utf-8'))
    except:
        pass

def connect_server(address):
    try:
        with client:
            client.connect(address)

            listener_message = th.Thread(target=received_message, args=(client,))
            listener_message.start()

            while True:
                message = input()
                client.sendall(message.encode('utf-8'))

                if message == 'salir':
                    print('Conexion cloed')
                    break
    except:
        print('Conexion cloed')
    

def main():
    connect_server((host, port))

if __name__ == '__main__':
    main()