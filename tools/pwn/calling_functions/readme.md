## 32 bits calling function with parameters

first we need to overwrite buffer then after that puting the address of function into the stack after that registers (edi,esi,edx) and finally the arguments

example : "a"\*44 + funct_addr + pop_edi_esi_edx_ret_addr + arg1 + arg2 + arg3

## 64 bits writing to a writable memory

one of the most useful gadget for that ''' mov qword ptr [r14], r15 ; ret '''

where + r15 : contains the strings we want to write (ex : "bin/sh") + r14 : contains memory address we want to write to (ex : .data section base address)
