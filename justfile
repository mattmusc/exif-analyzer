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
    python -m venv .venv
    {{ pip }} install --upgrade pip
    {{ pip }} install -e .

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
# Clean
# ─────────────────────

clean:
    rm -rf .venv
    rm -rf **/__pycache__
    rm -rf *.egg-info
