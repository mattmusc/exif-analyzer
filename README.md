# exif-analyzer

`exif-analyzer` is a CLI tool and Python library to analyze large photo archives
by extracting useful statistics from EXIF metadata
(focal lengths, cameras, ISO, apertures, shutter speeds, etc.).

It is designed to be:
- fast (batch processing + parallelism + exiftool)
- modular (clean separation between builders, renderers, and runner)
- usable both as a CLI tool and as a library
- easily extensible (JSON, CSV, API, dashboards)

---

## Features

- Analyze thousands of RAW/JPEG images
- 35mm equivalent focal length support
- Optional intelligent focal length bucketing
- Statistics for:
  - focal lengths
  - cameras
  - focal lengths by camera
  - ISO
  - apertures
  - shutter speeds
- Output formats:
  - console (readable tables)
  - JSON (machine-friendly)
- Clean architecture (builders / renderers / runner)
- Based on `exiftool` (via `PyExifTool`)

---

## Requirements

- Python ≥ 3.10
- `exiftool` installed system-wide

On macOS:
```bash
brew install exiftool
```

## Installation

The project uses `just` as a command runner. To set up the development environment:

```bash
just setup
```

This will create a virtual environment (`.venv`), upgrade pip, and install the package in editable mode with development dependencies.

## CLI Usage

You can run the analyzer directly through `just` or by calling the module:

```bash
# Basic analysis of the current directory
just analyze

# Analyze a specific directory
just analyze path/to/photos

# Change top N results and output format
just analyze-json path/to/photos

# Use raw focal lengths (no bucketing)
python3 -m exif_analyzer path/to/photos --no-bucket-focals

# Save results to a file
python3 -m exif_analyzer path/to/photos --format json --output stats.json
```

### Options:
- `-n, --top-n`: Number of top results to show (default: 10)
- `-e, --extensions`: List of extensions to scan
- `--no-bucket-focals`: Disable intelligent focal length grouping
- `--format`: `console` (default) or `json`
- `--output`: Save output to a specific file

---

## Architecture

`exif-analyzer` follows a clean, modular architecture:

- `cli.py`: Command-line argument definition.
- `runner.py`: Orchestration of the analysis pipeline.
- `metadata_extractor.py`: Multi-threaded metadata extraction via `exiftool`.
- `summaries_builders.py`: Logic for computing statistics (pure functions).
- `summaries_emitter.py`: Strategy for outputting the report.
- `renderers/`: Implementation of different output formats (Console, JSON).
- `files_retriever.py`: Recursive file discovery and filtering.

---

## Library usage

If you want to integrate `exif-analyzer` into your own Python scripts:

```python
from exif_analyzer.runner import run
from exif_analyzer.cli import parse_args

# Create a custom arguments namespace
args = parse_args(["/path/to/photos", "--top-n", "5"])
metadata = run(args)
```

---

## Development

We keep the project robust with a full test suite and linting tools.

```bash
# Run all tests
just test

# Run tests with coverage report
just cov

# Generate HTML coverage report
just cov-html

# Formatting and linting
just tools  # Install tools
just fmt    # Run black
just lint   # Run ruff
```

Current test coverage is **>90%** 🚀

---

## Roadmap
- [ ] CSV output
- [ ] SQLite backend
- [ ] Web dashboard

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
