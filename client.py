from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import Tkinter as tk


def receive():
    """saat menerima pesan akan melakukan ini"""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:  # saat client telah keluar
            break


def send(event=None):  
    """saat pesan dikirimkan akan melakukan ini"""
    msg = my_msg.get()
    my_msg.set("")  # mengosongkan input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """fungsi ini ketika window ditutup."""
    my_msg.set("{quit}")
    send()

top = tk.Tk()
top.title("iChat")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # scrollbar untuk navigasi vertical

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#bagian socketnya
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # untuk menampilkan GUI