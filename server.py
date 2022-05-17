import socket
import threading
import sys
import netifaces as ni

def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                targets = f.readlines()
                PORT = int(targets[0].rstrip())
        except FileNotFoundError:
            PORT = int(sys.argv[1])
    else:
        print('incorrect number arguments')
        exit(0)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
    try:
        server.bind((IP, PORT))
    except:
        print("The server cannot be started")
    server.listen(2)
    print(f'[*] Listening on {IP}:{PORT}')
    while True:
        try:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            client_handler = threading.Thread(target=handle_client, args=(client, address))
            client_handler.start()
        except KeyboardInterrupt:
            print("SIGINT.SERVER CLOSE CONNECTION!")
            break
    server.close()


def handle_client(client_socket, address):
    message = ''
    with client_socket as sock:
        while message != 'quit':
            try:
                request = sock.recv(1024)
                message = request.decode("utf-8")
                print(f'[*] Received: {message}')
                sock.send(f'Response from server echo-message: {message}'.encode())
            except BrokenPipeError:
                print(f'Client:{address[0]}:{address[1]} close connection.Bye!')
                break


if __name__ == '__main__':
    main()
