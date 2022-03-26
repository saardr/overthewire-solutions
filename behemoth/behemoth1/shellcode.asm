section .text

global _start
_start:
  push 0x0068732f ; '/sh'
  push 0x6e69622f ; '/bin'
  ; now '/bin/sh' is at esp
  mov ebx, esp    ; now ebx points to '/bin/sh'
  xor ecx, ecx
  xor edx, edx
  mov eax, 11     ; execve syscall
  int  0x80
