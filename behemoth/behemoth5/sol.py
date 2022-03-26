import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 1337))

data, addr = socket.recvfrom(1024)
print(data)
