from modbusclient import AtomicType

FLOAT = AtomicType("f", nan=-1., swap_words=True)
UCHAR = AtomicType("B", nan=0xFF)
U16 = AtomicType("H", nan=0xFFFF)
I16 = AtomicType("h")
WORD = U16
U32 = AtomicType("I", nan=0xFFFFFFFF)

