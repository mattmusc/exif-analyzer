# justfile

set dotenv-load := false

python := ".venv/bin/python"
pip := ".venv/bin/pip"

default:
    @just --list

# ─────────────────────
# Setup
# ─────────────────────

setup:
    /usr/bin/env python3 -m venv .venv
    {{ pip }} install --upgrade pip
    {{ pip }} install -e .
    {{ pip }} install -e ".[dev]"

# ─────────────────────
# Run
# ─────────────────────

analyze path=".":
    {{ python }} -m exif_analyzer {{ path }}

analyze-json path=".":
    {{ python }} -m exif_analyzer {{ path }} --format json

# ─────────────────────
# Dev
# ─────────────────────

fmt:
    {{ pip }} install black
    black exif_analyzer

lint:
    {{ pip }} install ruff
    ruff check exif_analyzer

tools:
    {{ pip }} install black ruff

# ─────────────────────
# Test
# ─────────────────────

test:
    .venv/bin/pytest

cov:
    .venv/bin/pytest --cov --cov-report=term-missing

cov-html:
    .venv/bin/pytest --cov --cov-report=html
    @echo "Open htmlcov/index.html"

# ─────────────────────
# Clean
# ─────────────────────

clean:
    rm -rf .venv
    rm -rf **/__pycache__
    rm -rf *.egg-info
    rm -rf htmlcov
