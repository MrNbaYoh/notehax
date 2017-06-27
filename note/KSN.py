include("../ropdb/DB.py")
import os

add_word(0x0)
add_word(ROP_OFFSET_KSN + os.path.getsize("../rop/build/rop.bin"))
org(0x1C + ROP_OFFSET_KSN)
incbin("../rop/build/rop.bin")
