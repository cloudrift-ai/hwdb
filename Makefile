PYTHON ?= python3

.PHONY: readme check test

readme:
	$(PYTHON) scripts/build_readme.py

check:
	$(PYTHON) scripts/build_readme.py --check

test:
	$(PYTHON) -m unittest discover -s tests
