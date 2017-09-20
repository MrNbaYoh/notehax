.section ".init"
.arm
.align 0x4
.global _start

_start:
	mov sp, #0x10000000
	blx _main
