import threading as th
import socket, pickle

host = '192.168.56.1'
port = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
state = None


# Server
def connect_server():
    global state, client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with client:
            client.connect((host, port))

            listener_message = th.Thread(target=received_message, args=(client,))
            listener_message.start()

            state = True            

            while state:
                message = str( input() )

                # Examplo of send of messages
                #send_message(["command1", "hello!!!!",message])
                send_message(["command2", "ke", "ondaa", message])

    except:
        close_server('Server Error')

def close_server(message = 'Server closed'):
    global state
    state = False
    client.close()
    print(message)


# Communication
def received_message(client):
    global message_decode, state

    try:
        while state:
            message = client.recv(1024)
            message_decode = pickle.loads(message)
            
            resultado = commands(message_decode)
            if resultado == False:
                break

    except:
        close_server('Server Error message')

def send_message(message):
    message_encode = pickle.dumps(message)
    client.sendall( message_encode )


def commands(message):
    command = message[0]
    arguments = message[1:len(message)]

    switcher = {
        'comando01': command01,
        'comando02': command02,
    }

    func = switcher.get(command, lambda: 'Invalid command')
    func(arguments)

    return True

## Commands Functions
def command01(args):
    print("Hello world:", args)

def command02(args):
    print("El server saluda: ", args)


# Main
def main():
    try:
        listener_message = th.Thread(target=connect_server)
        listener_message.start()
        
    except:
        print("Se detuvo todo inesperadamente")

if __name__ == '__main__':
    main()