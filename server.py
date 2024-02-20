import socket
import threading
import tkinter as tk

def start_server():
    global server_socket, clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    chat_area.insert(tk.END, "Очікування підключення...\n")

    while True:
        client_socket, client_address = server_socket.accept()
        chat_area.insert(tk.END, f"Підключено до {client_address}\n")
        clients.append(client_socket)
        threading.Thread(target=lambda: handle_client(client_socket)).start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            chat_area.insert(tk.END, f"Клієнт: {message}\n")
            broadcast_message(message, client_socket)
        except OSError:
            break

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                continue

def send_message():
    message = message_entry.get()
    chat_area.insert(tk.END, f"Ви: {message}\n")
    broadcast_message(message, None)
    message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Сервер")

chat_area = tk.Text(root, wrap=tk.WORD, width=40, height=10)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Entry(root, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

tk.Button(root, text="Відправити", command=send_message).grid(row=1, column=1, padx=10, pady=10)

server_socket = None
clients = []

threading.Thread(target=start_server).start()

root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()
