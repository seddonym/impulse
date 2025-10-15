# List available recipes.
help:
    @just --list

# Set up Git precommit hooks for this project (recommended).
install-precommit:
    @uv run pre-commit install

# Runs a smoke test under the latest supported Python version.
# This will open up a window showing the graph.
smoke-test:
    @uv run impulse drawgraph grimp

# Runs tests under all supported Python versions.
smoke-test-all: test-3-9 test-3-10
# Note that all recipes called from this must use UV_LINK_MODE=copy,
# otherwise the parallelism can corrupt the virtual environments.

# Runs tests under Python 3.9.
test-3-9:
    @UV_LINK_MODE=copy UV_PYTHON=3.9 just smoke-test

# Runs tests under Python 3.10.
test-3-10:
    @UV_LINK_MODE=copy UV_PYTHON=3.10 just smoke-test

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

# Build docs.
build-docs:
    @uv run --group=docs sphinx-build -b html docs dist/docs --fail-on-warning --fresh-env --quiet

# Build docs and open in browser.
build-and-open-docs:
    @just build-docs
    @open dist/docs/index.html

# Run all linters, build docs and smoke tests.
check:
    @UV_PYTHON=3.10 just lint  # See .github/workflows/main.yml for why.
    @just lint
    @just build-docs
    @just smoke-test-all
    @echo '👍 {{GREEN}} Linting, docs and smoke tests all good.{{NORMAL}}'