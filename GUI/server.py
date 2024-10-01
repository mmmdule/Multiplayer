import socket
import threading
import os

clients = []
values = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
move = 0


def print_matrix():
    string = f"{values[0]}║{values[1]}║{values[2]}\n═╬═╬═\n{values[3]}║{values[4]}║{values[5]}\n═╬═╬═\n{values[6]}║{values[7]}║{values[8]}"
    return string

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established!")
    global move
    while True:
        try:
            message = int(client_socket.recv(1024).decode('utf-8'))
            if client_socket == clients[move] and values[message - 1] == ' ':
                values[message - 1] = 'O' if move == 1 else 'X'
                move = 1 if move == 0 else 0
                #if not message:
                #    break
                print(f"{client_address}: {message}")
                broadcast(print_matrix(), client_socket)
            else:
                print (f"{client_address}: Tried to make an illegal move")
                broadcast(print_matrix(), client_socket) #da bi se ocistio display client-a
            os.system("cls")
            print(print_matrix())
        except Exception as error:
            clients.remove(client_socket)
            client_socket.close()
            print(error)
            break

def broadcast(message, sender_socket):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)
            client.close()

def main():    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(2)
    print(f"Server address is {socket.gethostbyname(socket.gethostname())}")
    print("Server is listening...")
    

    while len(clients) < 2:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    for client in clients:
        client_thread.join()

    server_socket.close()


if __name__ == "__main__":
    main()
