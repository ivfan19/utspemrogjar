from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """untuk penerimaan client"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s telah masuk." % client_address)
        client.send(bytes("Halo! Masukan nama anda", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # mengambil argumen klien, ip dll
    """menghandle satu akses dari satu client"""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! Jika ingin keluar, type {esc} lalu kirim.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s telah bergabung!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{esc}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{esc}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s telah meninggalkan room." % name, "utf8"))
            break


def broadcast(msg, prefix=""): 
    """Broadcasts pesan ke semua client"""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Menunggu koneksi klien...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
