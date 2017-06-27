export PYROP:="$(CURDIR)/pyrop"

all: ropdb/DB.py code/build note/build notehax

ropdb/DB.py:
	@cp ropdb/$(REGION).py ropdb/DB.py

code/build:
	@cd code && make

note/build: rop/build
	@cd note && make

notehax: note/build
	@cp note/build/note.bin utils/note.bin
	@cd utils && python signKWZ.py note.bin
	@mv utils/note.bin notehaxnotehaxnotehaxnotehax.kwz

rop/build:
	@cd rop && make

clean:
	@rm notehaxnotehaxnotehaxnotehax.kwz
	@rm ropdb/DB.py
	@cd note && make clean
	@cd rop && make clean
	@cd code && make clean
