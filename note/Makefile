all: build/KFH.bin build/KSN.bin build/note.bin

build/KFH.bin: KFH.py
	@python3 $(PYROP)/pyrop.py KFH.py build/KFH.bin

build/KSN.bin: KFH.py
	@python3 $(PYROP)/pyrop.py KSN.py build/KSN.bin

build/note.bin: note.py
	@python3 $(PYROP)/pyrop.py note.py build/note.bin

clean:
	@rm -rf build
