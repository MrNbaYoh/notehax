from constants import *
include("../ropdb/DB.py")

def garbage(n):
    for i in range(n):
        add_word(0xDEAC0DE)

def sleep(time_l, time_h=0):
    SET_LR(NOP)
    pop(r0=time_l, r1=time_h)
    add_word(SVC_SLEEPTHREAD)

@pop_macro
def POP_R0(r0):
    add_word(POP_R0PC)
    add_word(r0)

@pop_macro
def POP_R1(r1):
    add_word(POP_R1PC)
    add_word(r1)

@pop_macro
def POP_R3(r3):
    add_word(POP_R3PC)
    add_word(r3)

@pop_macro
def POP_R4(r4):
    add_word(POP_R4PC)
    add_word(r4)

@pop_macro
def POP_R11(r11):
    add_word(POP_R11PC)
    add_word(r11)

def SET_LR(lr):
    POP_R1(NOP)
    add_word(POP_R4LR_BX_R1)
    add_word(0xDEADC0DE) #r4 garbage
    add_word(lr)

@pop_macro
def POP_R4R5(r4, r5):
    add_word(POP_R4R5PC)
    add_word(r4)
    add_word(r5)


@pop_macro
def POP_R4R6(r4, r6):
    add_word(POP_R4R6PC)
    add_word(r4)
    add_word(r6)

@pop_macro
def POP_R0R1R2R3R4(r0, r1, r2, r3, r4):
    add_word(POP_R0R1R2R3R4PC)
    add_word(r0)
    add_word(r1)
    add_word(r2)
    add_word(r3)
    add_word(r4)

@pop_macro
def POP_R1R2R3R4R5(r1, r2, r3, r4, r5):
    add_word(POP_R1R2R3R4R5PC)
    add_word(r1)
    add_word(r2)
    add_word(r3)
    add_word(r4)
    add_word(r5)

@pop_macro
def POP_R1R2R3R4R5R6R7(r1, r2, r3, r4, r5, r6, r7):
    add_word(POP_R1R2R3R4R5R6R7PC)
    add_word(r1)
    add_word(r2)
    add_word(r3)
    add_word(r4)
    add_word(r5)
    add_word(r6)
    add_word(r7)

@pop_macro
def POP_R3R4R5R6R7R8R9(r3, r4, r5, r6, r7, r8, r9):
    add_word(POP_R3R4R5R6R7R8R9PC)
    add_word(r3)
    add_word(r4)
    add_word(r5)
    add_word(r6)
    add_word(r7)
    add_word(r8)
    add_word(r9)

@pop_macro
def POP_R4R5R6R7R8R9R10R11(r4, r5, r6, r7, r8, r9, r10, r11):
    add_word(POP_R4R5R6R7R8R9R10R11PC)
    add_word(r4)
    add_word(r5)
    add_word(r6)
    add_word(r7)
    add_word(r8)
    add_word(r9)
    add_word(r10)
    add_word(r11)

@pop_macro
def POP_R4R5R6R7R8R9R10R11R12(r4, r5, r6, r7, r8, r9, r10, r11, r12):
    add_word(POP_R4R5R6R7R8R9R10R11R12PC)
    add_word(r4)
    add_word(r5)
    add_word(r6)
    add_word(r7)
    add_word(r8)
    add_word(r9)
    add_word(r10)
    add_word(r11)
    add_word(r12)

def nop():
    add_word(NOP)

def deref_r0():
    add_word(LDR_R0R0_POP_R4PC)
    garbage(1)

def deref_to_r0(addr):
    pop(r0=addr)
    deref_r0()

def store_r0_to(addr):
    pop(r1=addr)
    add_word(STR_R0R1_POP_R4PC)
    garbage(1)

def store(val, addr):
    pop(r0=val)
    store_r0_to(addr)

def store_byte(val, addr):
    pop(r0=val, r4=addr)
    add_word(STRB_R0R4_POP_R4PC)
    garbage(1)

def deref_and_store(dst, src):
    pop(r0=src, r1=dst)
    add_word(LDR_R0R0_STR_R0R1_POP_R4PC)
    garbage(1)

def add_r0(val):
    pop(r4=val)
    add_word(ADD_R0R0R4_POP_R4PC)
    garbage(1)

def compare_r0(val):
    pop(r1=val)
    add_word(CMP_R0R1_MOVGT_R0_1_MOVLE_R0_0_POP_R4PC)
    garbage(1)

def memcmp(ptr1, ptr2, size):
    SET_LR(NOP)
    pop(r0=ptr1, r1=ptr2, r2=size)
    add_word(LMSI_MEMCMP+0x10)
    garbage(2)

def store_eq(val, addr):
    pop(r0=val, r4=addr-0x2C)
    add_word(STREQ_R0R4_2C_POP_R4PC)
    garbage(1)

def stack_pivot(sp,):
    pop(r0=sp, r1=NOP)
    add_word(MOV_SP_R0_MOV_R0R2_MOV_LRR3_BX_R1)

def flush_dcache(addr, size):
    pop(r0=addr, r1=size)
    add_word(GSPGPU_FLUSHDATACACHE_WRAPPER+0x4)
    garbage(3)

def mount_sdmc(sdmc_str):
    POP_R0(sdmc_str)
    add_word(FS_MOUNTSDMC + 0x4)
    garbage(3)

def try_open_file(ctx_ptr, file_path_ptr, openflags):
    pop(r0=ctx_ptr, r1=file_path_ptr, r2=openflags)
    add_word(FS_TRYOPENFILE + 0x4)
    garbage(5)


def try_get_size(ctx_ptr, out_size):
    pop(r0=ctx_ptr, r1=out_size)
    add_word(FS_TRYGETSIZE + 0x4)
    garbage(2)

@macro
def try_read_file(ctx_ptr, offseth, offsetl, out_bytes_read, size_ptr, dest):
    deref_and_store(FilePtr, ctx_ptr)
    deref_and_store(Size, size_ptr)

    pop(r0=out_bytes_read, r2=offsetl, r3=offseth)

    add_word(POP_R1PC)
    put_label("FilePtr")
    add_word(0xDEADC0DE)

    add_word(FS_TRYREADFILE + 0x4)
    garbage(6)
    add_word(POP_R4R5PC)
    add_word(dest)
    put_label("Size")
    add_word(0xDEADC0DE)


def close_file(ctx_ptr):
    SET_LR(NOP)
    POP_R0(ctx_ptr)
    add_word(FS_CLOSEFILE + 0x4)
