import socket
import sys
import netifaces as ni

def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                targets = f.readlines()
                target_host = targets[0].rstrip()
                target_port = int(targets[1].rstrip())
                target_port_client = int(targets[2].rstrip())
        except FileNotFoundError:
            print('File not found')
            exit(0)
    elif len(sys.argv) == 4:
        target_host = sys.argv[1]
        target_port = int(sys.argv[2])
        target_port_client = int(sys.argv[3])
    else:
        print('incorrect number arguments')
        exit(0)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((ni.ifaddresses('ens33')[ni.AF_INET][0]['addr'], target_port_client))
    try:
        client.connect((target_host, target_port))
    except OSError:
        print("Server not found")
        exit(1)
    print("Enter 'quit' to log out from the server")
    message = input('Enter message:')
    while message != 'quit':
        try:
            client.send(message.encode())
            response = client.recv(4096)
            print(response.decode())
            message = input('Enter message:')
        except KeyboardInterrupt:
            print('SIGINT:Client close connection')
            break
    client.close()
    return 0


if __name__ == '__main__':
    main()
