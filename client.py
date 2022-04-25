import socket


def main():
    target_host = int(input("enter the server address"))
    target_port = int(input("Enter the server port"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    print("Enter 'quit' to log out from the server")
    message = input()
    while message != 'quit':
        client.send(message)
        response = client.recv(4096)
        print(response.decode())
        message = input()
    client.close()