## 32 bits calling function with parameters

first we need to overwrite buffer then after that puting the address of function into the stack after that registers (edi,esi,edx) and finally the arguments

example : "a"\*44 + funct_addr + pop_edi_esi_edx_ret_addr + arg1 + arg2 + arg3
