flake8-check:
	flake8 --config=.flake8

isort-check:
	isort -rc -c . --diff

black:
	black . --config pyproject.toml

isort:
	isort -rc .

linters-check: isort-check black-check flake8-check

linters: isort black flake8-check
