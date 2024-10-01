import tkinter as tk
from tkinter import messagebox
import socket
import threading
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buttons = []
def open_new_window():
    prozor=tk.Toplevel(root)
    prozor.title("3x3 Button Grid")
    frame = tk.Frame(prozor)
    frame.pack(pady=20)

    # Create 3x3 grid of buttons
    button_number = 1
    for i in range(3):
        for j in range(3):
            create_button(frame, button_number, i, j)
            button_number += 1

def setButtons(message):
    global buttons
    rows = message.split("\n")
    rows.pop(1)
    rows.pop(2)
    index= 0
    for row in rows:
        values = row.split("║")
        buttons[index]["text"] = values[0]
        buttons[index+1]["text"] = values[1]
        buttons[index+2]["text"] = values[2]
        index += 3

def receive_messages(client_socket):
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if len(message)==1:
                messagebox.showinfo("Kraj igre",f"Pobedio je igrac broj {message}.")
                client_socket.close()
                quit()

            print(f"{message}")
            setButtons(message)
        except Exception as e:
            print(e)
            print("Connection closed by the server.")
            client_socket.close()
            break

def connect_to_server_thread():
    thread=threading.Thread(target=connect_to_server)
    thread.start()
def connect_to_server():
    global client_socket
    ip_address = ip_entry.get()
    try:
        client_socket.connect((ip_address, 12345))  # Replace 12345 with your server's port
        messagebox.showinfo("Connection Status", "Connected to the server successfully!")
        open_new_window()
        receive_messages(client_socket)

    except Exception as e:
        messagebox.showerror("Connection Status", f"Failed to connect to the server: {e}")

def send_message(number):
    global client_socket
    try:
        client_socket.send(str(number).encode('utf-8'))
    except Exception as e:
        print(f"Failed to send message: {e}")

def create_button(frame, text, row, col):
    global buttons
    button = tk.Button(frame, width=10, height=3, command=lambda: send_message(text))
    button.grid(row=row, column=col, padx=5, pady=5)
    buttons.append(button)



root = tk.Tk()
root.title("Server Connection")
root.geometry("300x150")

ip_label = tk.Label(root, text="Enter Server IP:")
ip_label.pack(pady=10)

ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

connect_button = tk.Button(root, text="Connect", command=connect_to_server_thread)
connect_button.pack(pady=20)

root.mainloop()
