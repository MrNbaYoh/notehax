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
	@cd utils && python3 signKWZ.py note.bin
	@mv utils/note.bin notehaxnotehaxnotehaxnotehax.kwz

rop/build:
	@cd rop && make

clean:
	@rm ropdb/DB.py
	@cd rop && make clean
	@cd code && make clean
	@cd note && make clean
	@rm notehaxnotehaxnotehaxnotehax.kwz
