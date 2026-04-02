PY ?= py
PYTEST ?= $(PY) -m pytest

.PHONY: test test1 test2 test3 main run

test: test1 test2 test3

test1:
	$(PYTEST) test/test1.py

test2:
	$(PYTEST) test/test2.py

test3:
	$(PYTEST) test/test3.py

main:
	$(PY) main.py

run: main
