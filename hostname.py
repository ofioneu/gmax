import socket
try:
	hostname = socket.gethostname()
	print(hostname)
except:
	print('Falha ao obter hostname!')