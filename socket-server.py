import threading as th
import socket, pickle


host = '192.168.56.1'
port = 65432

list_clients = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Server
def start_server():
    try:
        server.bind((host, port))
        server.listen()
        print('Server on', (host, port))

        while True:
            conn, addr = server.accept()
            add_client(conn, addr)
    except:
        disconnect_server()

def disconnect_server():
    disconnect_all_clients()
    server.close()
    print('Server closed')


# Client
def add_client(client, addr):
    client_number = len(list_clients)
    uid = str(addr[0])+":"+str(client_number)
    hilo_esuccha = th.Thread(target=listener_mesagges, args=(client, uid))

    list_clients[uid] = {
        'client': client, 
        'addr': addr,
        'hilo_esuccha': hilo_esuccha,
    }
    
    hilo_esuccha.start()

    print('{} CONNECTED, addr: {}'.format(uid, addr))
    send_message(uid, 'Server', ['comando01','Bienvenido al server!'])

def disconnect_client(uid):
    try:
        list_clients[uid]['client'].close()
        del list_clients[uid]
        print('{} DISCONNECTED'.format(uid))
    except:
        pass

def disconnect_all_clients():
    for uid in list_clients:
        send_message(uid, 'Server', 'Disconnect')
        list_clients[uid]['client'].close()


# Communication
def listener_mesagges(client, uid):
    try:
        while True:
            message = client.recv(1024)
            message_decode = pickle.loads(message)
            if message_decode == '':
                break

            resultado = commands(uid, message_decode)
            if resultado == False:
                break
   
    except:
        disconnect_client(uid)

def send_message(client_uid, from_uid, message, hideConsole=False):
    if not hideConsole:
        print('{} {} SEND: {}'.format(client_uid, from_uid, message))

    message_encode = pickle.dumps(message)
    list_clients[client_uid]['client'].send(message_encode)


# Commands
def commands(uid, message):
    command = message[0]
    arguments = message[1:len(message)]     # Jala todos los elementos del array sin tomar en cuenta el primer valor.
    arguments.insert(len(arguments), uid)   # Le inserta como ultimo el argumento la id del client.

    switcher = {
        'command1': command01,
        'command2': command02,
    }

    func = switcher.get(command, lambda: 'Invalid command')
    func(arguments)

    return True

## Commands Functions
def command01(args):
    print("Hello world:", args)

def command02(args):
    print("Este es el comando 2 !", args)


# Main
def main():
    try:
        start_server()
    except:
        print("Se detuvo todo inesperadamente")

if __name__ == '__main__':
    main()