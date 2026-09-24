# PyForge

Developer & System Utility Toolkit written in Python.

## Overview

PyForge collects practical file, text, encoding, hashing, JSON, network,
system, developer, Git, and defensive security utilities in one local-first
terminal application. School Purpose Only.

## Features

Features are implemented as small, independently testable functions and
exposed through both an interactive Rich menu and Typer commands.

## Installation

Requires Python 3.12 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Quick Start

Run `python main.py` for the command interface, `pyforge interactive` for the
numbered Rich menu, or `pyforge --help` for command details.

## Commands

- `pyforge categories` lists categories.
- `pyforge tools [CATEGORY]` lists registered utilities.
- `pyforge search QUERY` finds matching utilities.
- `pyforge describe TOOL` shows metadata for one utility.
- `pyforge run TOOL --arguments '{"name":"value"}'` executes one utility.
- `pyforge export TOOL --format json` exports a result.
- `pyforge history` displays local execution metadata.

## File Tools

Metadata, hashing, comparison, duplicates, directory summaries and trees,
search, size checks, empty-file checks, extension statistics, and snapshots.

## Text Tools

Statistics, counts, duplicate detection, diffs, cleanup, case conversion,
slug generation, sorting, search, and regular-expression testing.

## Encoding

Base64, URL, hexadecimal, and HTML encode/decode operations with validation.

## Hashing

Text and file hashing supports MD5, SHA-1, SHA-256, SHA-384, and SHA-512.
MD5 and SHA-1 are included only for compatibility and file identification;
do not use them for password storage or security-sensitive integrity guarantees.

## JSON

Formatting, minification, validation, viewing, statistics, key search, and
structural comparison.

## Networking

Safe DNS, local interface, public IP, HTTP header/status, and URL inspection
with bounded timeouts. No offensive scanning functionality is included.

## System

CPU, memory, disk, operating system, redacted environment, process, listening
port, uptime, and Python environment information for the local machine.

## Developer Tools

UUIDs, timestamps, random strings, colors, cron explanations, project trees,
source counts, and adapters for JSON, regex, URL, and environment workflows.

## Git Tools

Read-only repository, branch, history, contributor, status, ignore, statistics,
and large tracked-file helpers. PyForge never rewrites Git history.

## Configuration

`config/settings.json` controls theme, history, default export format, HTTP
timeout, and advanced information. Invalid or corrupted settings safely fall
back to validated defaults.

## Exports

Suitable tool results can be exported as TXT, JSON, or CSV under `exports/`.
Generated exports are ignored by Git.

## Testing

Run `pytest` for the complete suite and `ruff check .` for correctness linting.
Network tests use mock transports and do not depend on public services.

## Architecture

Tool functions live under `pyforge/tools/`; `registry.py` provides lazy
discovery, `ui/` owns Rich rendering, `storage/` owns SQLite history, and
`services/exporter.py` owns export formats. See `docs/architecture.md`.

## Security

Security utilities are defensive and intended only for authorized systems,
files, and domains. Secret findings are never transmitted. School Purpose Only.

## Privacy

History excludes arguments and raw inputs. Passwords, tokens, secrets, and file
contents are not stored. Network access occurs only for explicitly selected
network and certificate tools.

## Contributing

Read `CONTRIBUTING.md`, keep changes focused, and add tests for behavior changes.

## License

PyForge is available under the MIT License. See `LICENSE`.
