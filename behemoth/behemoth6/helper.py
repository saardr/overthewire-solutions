def get_hex_representation(s):
    s = s.encode()
    while len(s) % 4 != 0:
        s += b'\0'
    s = s[::-1]
    push_blocks = []
    for i in range(0, len(s), 4):
        push_blocks.append(s[i:i+4])
    for block in push_blocks:
        s = "0x"
        for c in block:
            s += hex(c)[2:]
        print(s)

# get_hex_representation("HelloKitty")

def print_shellcode_to_file(filename):
    f = open(filename, 'wb')
    shellcode_hex = open("shellcode_hex.txt").read()
    shellcode_hex = shellcode_hex.replace('\n', ' ')
    shellcode_hex_arr = shellcode_hex.split(' ')
    shellcode_arr = bytearray(int(num, 16) for num in shellcode_hex_arr)
    f.write(shellcode_arr)
    f.close()

print_shellcode_to_file("shellcode.txt")