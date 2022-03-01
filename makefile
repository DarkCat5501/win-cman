.PHONY: all

all:
	lib

lib: src/library.py
	@call python .\src\library.py
	@echo program exited with code (%ERRORLEVEL%)
