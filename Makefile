VENV ?= .venv
PYTHON ?= $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)

.PHONY: setup readme check test

setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r requirements.txt

readme:
	$(PYTHON) scripts/build_readme.py

check:
	$(PYTHON) scripts/build_readme.py --check

test:
	$(PYTHON) -m unittest discover -s tests
