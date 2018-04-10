import socket
import ssl
import threading


class Server(object):
    """"
    Constructor of Server class, takes ip address, port, path to private key and to certificate
    """
    def __init__(self, host, port, keyfile, certfile):

        self.host = host
        self.port = port
        self.max_awaiting_connections = 25
        self.client_timeout_sec = 60
        self.keyfile = keyfile
        self.certfile = certfile
        self.is_running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock_ssl = ssl.wrap_socket(self.sock, keyfile=self.keyfile, certfile=self.certfile, server_side=True)

    """
    Function opens a connection on specified port. When there is an incoming connection socket accepts it on separate thread.
    """
    def listen(self):

        self.sock_ssl.listen(self.max_awaiting_connections)
        self.is_running = True
        print("Server running")
        while True:
            client, address = self.sock_ssl.accept()
            client.settimeout(self.client_timeout_sec)
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    """
    Function handles client data and sends a response to him
    """
    def listenToClient(self, client, address):

        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = "Data received"
                    client.send(response)
                else:
                    raise error("Client disconnected")
            except:
                client.close()
                return False
