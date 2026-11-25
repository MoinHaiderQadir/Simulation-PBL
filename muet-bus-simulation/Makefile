.PHONY: install verify quick full test clean
install:
	pip install -r requirements-dev.txt
verify:
	python tests/verify.py
test:
	pytest -q
quick:
	python src/experiments.py --quick
full:
	python src/experiments.py
clean:
	find . -name __pycache__ -prune -exec rm -rf {} +
