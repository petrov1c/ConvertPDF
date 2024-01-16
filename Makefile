.PHONY: lint
lint:
	flake8 ./

.PHONY: app
app:
	python3 ./run.py
