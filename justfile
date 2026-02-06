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
    {{ python }} -m black exif_analyzer

lint:
    {{ python }} -m ruff check exif_analyzer

# ─────────────────────
# Test
# ─────────────────────

test:
    {{ python }} -m pytest

cov:
    {{ python }} -m pytest --cov=exif_analyzer --cov-report=term-missing

cov-html:
    {{ python }} -m pytest --cov=exif_analyzer --cov-report=html
    @echo "Open htmlcov/index.html"

# ─────────────────────
# Clean
# ─────────────────────

clean:
    /usr/bin/env python3 scripts/clean.py

deep-clean:
    /usr/bin/env python3 scripts/clean.py --venv

# ─────────────────────
# CI
# ─────────────────────

ci: lint cov
