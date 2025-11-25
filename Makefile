# Install all dependencies
install:
	pip install -r requirements-dev.txt

# Run tests with pytest
tests:
	pytest -q -s

# Run code style and lint checks
lint:
	black .
	flake8 .
