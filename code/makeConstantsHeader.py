import sys
import runpy

cmdargs = sys.argv

output_file = open(cmdargs[2], 'w')

result = runpy.run_path(cmdargs[1])
diff = set(result.keys()) - set(globals().keys())

for gadget in diff:
    output_file.write("#define " + gadget + " " + hex(result[gadget]) + "\n")
