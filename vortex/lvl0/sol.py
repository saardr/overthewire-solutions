#!/usr/bin/env python3

import socket
import struct

addr = "vortex.labs.overthewire.org"
port = 5842

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((addr, port))

packed_nums = [0 for i in range(4)]
for i in range(4):
  packed_nums[i] = sock.recv(4) 

unpacked_nums = [struct.unpack("I", num)[0] for num in packed_nums]
res = sum(unpacked_nums)

print(res)
res_packed = struct.pack('L', res)
sock.sendall(res_packed)
final = sock.recv(1024)
print(final)
