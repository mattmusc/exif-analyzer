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

## Architecture

```
exif_analyzer/
├─ cli.py                 # argument parsing
├─ runner.py              # orchestration
├─ metadata_extractor.py  # exiftool + parallel processing
├─ summaries_builders.py  # statistics computation (pure functions)
├─ summaries_emitter.py   # output selection
├─ renderers/
│  ├─ console.py
│  └─ json.py
└─ files_retriever.py
```

## Library usage

```python
from exif_analyzer.runner import run
from exif_analyzer.cli import parse_args

args = parse_args()
run(args)
```
