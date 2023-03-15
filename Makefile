SHELL = /bin/bash -c
VIRTUAL_ENV = $(shell poetry env info -p)
export BASH_ENV=$(VIRTUAL_ENV)/bin/activate

.DEFAULT_GOAL:=help
.PHONY: help
help:  ## Display this help
	$(info  AI Git Commit is a Python-based tool that uses AI to generate Git commit messages automatically.)
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

pyproject.toml:
	$(info Create pyproject.toml file...)
	poetry init \
		--no-interaction --quiet \
		--name "ai-git-commit" \
		--description " AI Git Commit is a Python-based tool that uses AI to generate Git commit messages automatically." \
		--license=MIT \
		--python ^3.9 \
		--dependency click \
		--dependency toml-cli \
		--dependency black \
		--dependency isort \
		--dependency pytest \
		--dependency pytest-cov \
		--dependency mypy \
		--dependency xenon \
		--dependency radon \
		--dependency twine

.git:
	git init
	pre-commit install

.PHONY: _poetry-install
_poetry-install:
	$(info Install all dependencies)
	poetry install

.PHONY: _poetry-config
_poetry-config:
	if [ -z $(shell cat pyproject.toml | grep tool.poetry.scripts) ]; then\
		echo "Initial setup detected, adding additional configuration..."; \
        poetry run toml add_section --toml-path pyproject.toml tool.poetry.scripts; \
		poetry run toml set --toml-path pyproject.toml tool.poetry.scripts.ai-git-commit "ai_git_commit:main"; \
		poetry run toml add_section --toml-path pyproject.toml tool.pytest; \
		poetry run toml set --toml-path pyproject.toml tool.pytest.testpaths "tests"; \
		poetry run toml add_section --toml-path pyproject.toml tool.mypy; \
		poetry run toml set --toml-path pyproject.toml tool.mypy.ignore_missing_imports TRUE; \
		poetry run toml add_section --toml-path pyproject.toml tool.coverage.run; \
		poetry run toml set --toml-path pyproject.toml tool.coverage.run.branch TRUE; \
		poetry run toml set --toml-path pyproject.toml tool.coverage.run.source SOURCE; \
		poetry run toml add_section --toml-path pyproject.toml tool.coverage.report; \
		poetry run toml set --toml-path pyproject.toml tool.coverage.report.show_missing TRUE; \
		poetry run toml set --toml-path pyproject.toml tool.coverage.report.fail_under COVERAGE; \
		poetry run toml set --toml-path pyproject.toml tool.coverage.report.exclude_lines EXCLUDE_LINES; \
		if [ -e "pyproject.toml" ]; then \
			sed 's/"TRUE"/true/g' pyproject.toml > tmpfile && mv tmpfile pyproject.toml; \
			sed 's/"COVERAGE"/100/g' pyproject.toml > tmpfile && mv tmpfile pyproject.toml; \
			sed 's/"SOURCE"/["ai_git_commit"]/g' pyproject.toml > tmpfile && mv tmpfile pyproject.toml; \
			sed 's/"EXCLUDE_LINES"/["if __name__ == .__main__.:"]/g' pyproject.toml > tmpfile && mv tmpfile pyproject.toml; \
			sed 's/"poetry-core"/"poetry-core>=1.1.0"/g' pyproject.toml > tmpfile && mv tmpfile pyproject.toml; \
		fi \
		git add .; \
		git commit -m "feat: initial commit"; \
    fi


.PHONY: install
install: pyproject.toml .git _poetry-install _poetry-config ## Install all dependencies

.PHONY: build
build:
	poetry build

.PHONY: release
release: build
	twine upload dist/*

.PHONY: _radon
_radon:
	$(info Maintenability index)
	radon mi --min A --max A --show --sort ai_git_commit

.PHONY: _xenon
_xenon:
	$(info Cyclomatic complexity index)
	xenon --max-absolute A --max-modules A --max-average A ai_git_commit

.PHONY: complexity-baseline
complexity-baseline: _radon _xenon ## Run the complexity baseline

.PHONY: lint
lint: _black _isort _mypy ## Lint all code

 .PHONY: _black
_black:
	$(info [*] Formatting python files with black...)
	black .

.PHONY: _isort
_isort:
	$(info [*] Formatting python files with isort...)
	isort .

.PHONY: _mypy
_mypy:
	$(info [*] Python static type checker...)
	mypy --junit-xml reports/typecheck.xml ai_git_commit

.PHONY: test
test: complexity-baseline ## Run the tests defined in the project
	pytest --cov

$(VERBOSE).SILENT:
