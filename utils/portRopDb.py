import sys
import re
import runpy

BASE_ADDR = 0x100000
cmdargs = sys.argv

src_codebin = open(cmdargs[1], 'rb').read()
dst_codebin = open(cmdargs[2], 'rb').read()
out_db = open(cmdargs[4], 'w')

glob = runpy.run_path(cmdargs[3])
gadgets = list(glob.keys() - globals().keys())
gadgets.sort()

letter = gadgets[0][0]

for g in gadgets:
    found = False
    while not found:
        print("Size of (in instructions, 0 to skip) : " + g  + " ?")
        size = int(input())
        if size == 0:
            found = True
            continue
        offset = glob[g] - BASE_ADDR
        pattern = src_codebin[offset:offset+4*size]
        new_off = dst_codebin.find(pattern)
        if new_off >= 0:
            if g[0] != letter:
                letter = g[0]
                out_db.write("\n")
            out_db.write(g + " = " + hex(new_off+BASE_ADDR) + "\n")
            found = True
            print("OK")
        else:
            print("NOT FOUND")
