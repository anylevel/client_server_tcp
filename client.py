import socket


def main():
    target_host = input("Enter the server address:")
    target_port = int(input("Enter the server port:"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
