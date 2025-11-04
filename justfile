# List available recipes.
help:
    @just --list

# Set up Git precommit hooks for this project (recommended).
install-precommit:
    @uv run pre-commit install

# Run tests under the latest supported Python version.
# This will open up a window showing the graph.
test:
    @uv run pytest
    @uv run impulse drawgraph grimp
    @uv run --with=google-cloud-audit-log impulse drawgraph google.cloud.audit
    @uv run impulse drawgraph grimp --show-import-totals
    @uv run --with=django impulse drawgraph django.db --show-cycle-breakers


# Run tests under all supported Python versions.
test-all: test-3-9 test-3-10 test-3-11 test-3-12 test-3-13 test-3-14

# Run tests under Python 3.9.
test-3-9:
    @UV_PYTHON=3.9 just test

# Run tests under Python 3.10.
test-3-10:
    @UV_PYTHON=3.10 just test

# Run tests under Python 3.11.
test-3-11:
    @UV_PYTHON=3.11 just test

# Run tests under Python 3.12.
test-3-12:
    @UV_PYTHON=3.12 just test

# Run tests under Python 3.13.
test-3-13:
    @UV_PYTHON=3.13 just test

# Run tests under Python 3.14.
test-3-14:
    @UV_PYTHON=3.14 just test

# Format the code.
format:
    @uv run ruff format

# Run linters.
lint:
    @echo Running ruff format...
    @uv run ruff format --check
    @echo Running ruff check...
    @uv run ruff check
    @echo Running mypy...
    @uv run mypy src/impulse tests
    @echo
    @echo '👍 {{GREEN}} Linting all good.{{NORMAL}}'

# Fix any ruff errors
autofix:
    @uv run ruff check --fix

# Build docs.
build-docs:
    @uv run --group=docs sphinx-build -b html docs dist/docs --fail-on-warning --fresh-env --quiet

# Build docs and open in browser.
build-and-open-docs:
    @just build-docs
    @open dist/docs/index.html

# Run all linters, build docs and smoke tests.
check:
    @just lint
    @just build-docs
    @just test-all
    @echo '👍 {{GREEN}} Linting, docs and smoke tests all good.{{NORMAL}}'

# Upgrade Python code to the supplied version. (E.g. just upgrade 310)
upgrade-python MIN_VERSION:
    @find {docs,src,tests} -name "*.py" -not -path "tests/assets/*" -exec uv run pyupgrade --py{{MIN_VERSION}}-plus --exit-zero-even-if-changed {} +
    @just autofix
    @just format
