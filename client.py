import socket
import threading
import tkinter as tk

def receive_messages():
    while True:
        chat_area.insert(tk.END, f"Інший: {server_socket.recv(1024).decode('utf-8')}\n")

def send_message():
    message = message_entry.get()
    chat_area.insert(tk.END, f"Ви: {message}\n")
    server_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Клієнт")

chat_area = tk.Text(root, wrap=tk.WORD, width=40, height=10)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Entry(root, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

tk.Button(root, text="Відправити", command=send_message).grid(row=1, column=1, padx=10, pady=10)

server_ip = input("Введіть IP-адресу сервера: ")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((server_ip, 12345))

threading.Thread(target=receive_messages).start()
root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()
