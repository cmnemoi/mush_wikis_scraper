all: setup-git-hooks install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

semantic-release:
	uv run semantic-release version --changelog --no-push --no-vcs-release --skip-build --no-commit

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	git config core.hooksPath hooks

test:
	uv run pytest -vv --cov=mush_wikis_scraper --cov-report=xml

.PHONY: all check check-format check-lint check-types install lint setup-git-hooks test