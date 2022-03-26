section .text

; HelloKitty

global _start
_start:
    push 0x00007974         ; ty\0\0
    push 0x74694b6f         ; oKit
    push 0x6c6c6548         ; Hell

    mov eax, 4              ; write syscall
    mov ebx, 1              ; stdout file descryptor
    mov ecx, esp            ; ebx now points to "HelloKitty\0\0"
    mov edx, 10             ; count = 10
    int 0x80

    mov eax, 1
    xor ebx, ebx
    int 0x80                ; exit(0)