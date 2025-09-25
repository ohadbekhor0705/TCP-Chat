
import threading
import socket
from cryptography.fernet import Fernet
class Client:
	def __init__(self,ip: int,port,name = "") -> None:
		self.name = name
		self.port = port
		self.ip = ip
		self.client: socket.socket = None
		self.connected = self.connect()
		self.f: Fernet = None
		with open("key.bin","rb") as key_file:
			self.f = Fernet(key_file.read())
	def connect(self) -> bool:
		#returns if the client mannage to connect to the serever
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.ip,self.port))
		except Exception as e:
			self.client = None
			return False
		return self.client is not None
	def disconnect(self):
		self.connected = False
		self.client = None
	def send_message(self, msg: str):
		token = self.f.encrypt(msg.encode("utf-8"))
		self.client.send(token)

	def recv(self) -> str:
		token: bytes = self.client.recv(1024)
		print("Encrypted message is: ",token)	
		received_message:str =  self.f.decrypt(token).decode("utf-8")
		return received_message
	