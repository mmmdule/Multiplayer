import socket
import threading
import os
import time

clients = []
values = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
move = 0

combo_indices = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

def reset_server():
    global clients
    for client in clients:
        client.close()
    clients.clear()

def game_won_by(board):
    winner = 0
    for index in combo_indices:
        if board[index[0]] == board[index[1]] == board[index[2]] != ' ':
            winner = 1 if board[index[0]] == 'X' else 2
    return winner

def print_matrix():
    string = f"{values[0]}║{values[1]}║{values[2]}\n═╬═╬═\n{values[3]}║{values[4]}║{values[5]}\n═╬═╬═\n{values[6]}║{values[7]}║{values[8]}"
    return string

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established!")
    global move
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        try:
            message = int(message)
        except:
            break
        if client_socket == clients[move] and values[message - 1] == ' ':
            values[message - 1] = 'O' if move == 1 else 'X'
            move = 1 if move == 0 else 0
            #if not message:
            #    break
            print(f"{client_address}: {message}")
            broadcast(print_matrix())
            if game_won_by(values) != 0:
                broadcast(str(game_won_by(values)))
                time.sleep(3)
                #reset_server()
                break
        else:
            print (f"{client_address}: Tried to make an illegal move")
            broadcast(print_matrix()) #da bi se ocistio display client-a
        os.system("cls")
        print(print_matrix())

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

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
