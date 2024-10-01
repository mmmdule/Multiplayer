import socket
import threading
import os

os.system("cls")

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            os.system("cls")
            print(f"{message}")
        except:
            print("Connection closed by the server.")
            client_socket.close()
            break

def main():
    ip = input("Unesite IP servera: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 12345))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input() # "Enter message to send: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()
