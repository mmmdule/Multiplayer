import tkinter as tk
from tkinter import messagebox
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    global client_socket
    ip_address = ip_entry.get()
    try:
        client_socket.connect((ip_address, 12345))  # Replace 12345 with your server's port
        messagebox.showinfo("Connection Status", "Connected to the server successfully!")
        open_new_window()
    except Exception as e:
        messagebox.showerror("Connection Status", f"Failed to connect to the server: {e}")

def send_message(number):
    global client_socket
    try:
        client_socket.send(str(number).encode('utf-8'))
    except Exception as e:
        print(f"Failed to send message: {e}")

def create_button(frame, text, row, col):
    button = tk.Button(frame, text=text, width=10, height=3, command=lambda: send_message(text))
    button.grid(row=row, column=col, padx=5, pady=5)

def open_new_window():
    root = tk.Tk()
    root.title("3x3 Button Grid")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Create 3x3 grid of buttons
    button_number = 1
    for i in range(3):
        for j in range(3):
            create_button(frame, button_number, i, j)
            button_number += 1

root = tk.Tk()
root.title("Server Connection")
root.geometry("300x150")

ip_label = tk.Label(root, text="Enter Server IP:")
ip_label.pack(pady=10)

ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

connect_button = tk.Button(root, text="Connect", command=connect_to_server)
connect_button.pack(pady=20)




root.mainloop()
