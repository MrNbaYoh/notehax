import binascii
import os

def add_chunk(name, b, file, need_crc):
    add_ascii(name)
    add_byte(b)
    add_word(os.path.getsize(file) + 4 if need_crc else 0)
    if(need_crc):
        add_word(binascii.crc32(open(file, 'rb').read()))
    incbin(file)
    align(4)

add_chunk("KFH", 0x14, 'build/KFH.bin', True) #file header
add_chunk("KTN", 0x02, '../res/preview.jpg', True) #picture for preview
add_chunk("KSN", 0x01, 'build/KSN.bin', False) #overflowed chunk+ropchain
