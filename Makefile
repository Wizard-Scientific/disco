# 0xidm

help:
	@echo The following makefile targets are available:
	@echo
	@grep -e '^\w\S\+\:' Makefile | sed 's/://g' | cut -d ' ' -f 1

install:
	pip install -U pip
	pip install -e .

test:
	pytest ./src

repl:
	./src/scripts/disco-manager.py repl

.PHONY: help requirements bot
