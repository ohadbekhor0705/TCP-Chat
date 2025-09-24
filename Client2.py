
import threading
import socket
class Client:
	def __init__(self,ip,port) -> None:
		self.name = ""
		self.port = port
		self.ip = ip
		self.client: socket.socket = None
		self.connected = False

	def start(self):
		display = self.display
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.ip,self.port))
			self.name = input("enter name: ")
			if self.name or self.name != "":
				self.connected = True
		except Exception as e:
			self.client = None
			print(e)
		while self.connected:
			t = threading.Thread(target=self.display)
			t.start()
			msg: str = f"{self.name}; " + input(f"{self.name}: ")
			self.send_message(msg)

	def send_message(self, msg: str):
		self.client.send(msg.encode("utf-8"))
		
	def recv(self) -> str:	
		data = self.client.recv(1024).decode()
		return data
	def display(self):
		while self.connected:
			data = self.recv()
			if data:
				print(data)


if __name__ == "__main__":
	port = int(input("Enter port:"))
	ip = "127.0.0.1"
	client = Client(ip,port)
	client.start()