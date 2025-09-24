import socket
import threading



client_list: set[ClientHandler] = set()



class ServerBL(threading.Thread):
    def __init__(self,IP: int, PORT: str) -> None:
        global client_list
        self.PORT = PORT
        self.IP = IP
        self.clients:set[ClientHandler] = client_list
        self.running: bool = False
        self.remove_event = "remove"
    
    def start(self) -> None: # this function start automatically when CClientHandler.start() (Inherits from threading.thread class)
        print(f"[SERVER] listing.... {socket.gethostbyname(socket.gethostname())},\n[PORT] {"."*13} {self.PORT}")
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.IP, self.PORT))
                s.listen()
                conn, addr = s.accept()
                client_handler: ClientHandler = ClientHandler(conn,addr,self.fire_event)
                client_handler.start()
                self.clients.add(client_handler)
    def messages_handler(self):
        while True:
            

    def fire_event(self, event: str): # Used for inheritance
        pass
    def send_to_all_clients(self, sender: socket.socket, message: bytes):
        for client_handler in self.clients:
            if client_handler.client != sender:
                if message.decode() == "!dis":
                    client_handler.client.send(f"{sender} disconnected from the chat".encode())
                else:
                    client_handler.client.send(message)

class ClientHandler(threading.Thread):
    def __init__(self, client_socket: socket.socket, address: socket._RetAddress, fn: function):
        super().__init__()
        self.addr = address
        self.client = client_socket
        self.fn = fn
    def run(self):  # this function start automatically when CClientHandler.start() (Inherits from threading.thread class)
        # This code run in separate thread for every client:
        connected = True
        while connected:
            try:
                message = self.client.recv(1024)
                if message:
                    print(f"[{self.addr}] {message.decode("utf-8")}")
                
            except ConnectionResetError:

                connected = False


