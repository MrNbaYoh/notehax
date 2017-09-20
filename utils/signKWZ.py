import sys
import os

cmdargs = sys.argv

file_path = cmdargs[1]
os.system("openssl dgst -sha256 -sign key.pem -out signature.bin " + file_path)

signature = open("signature.bin", "rb").read()
open(file_path, "ab").write(signature)
os.remove("signature.bin")
