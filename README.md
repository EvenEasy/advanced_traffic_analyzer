# Advanced Traffic Analyzer

A small command-line tool to analyze web server access logs. It supports
filtering, aggregation and basic reporting to help inspect traffic patterns,
top clients, and response metrics.

## Input format

Each log line must contain six whitespace-separated fields in the following
order:

- timestamp: integer UNIX timestamp
- ip_address: client IP address (string)
- http_method: HTTP method (e.g. GET, POST)
- url: requested URL
- status_code: integer HTTP status code
- response_size: integer number of bytes in the response

Example line:

1615564800 192.0.2.1 GET /index.html 200 5120

## Installation

This project is pure Python. Create a virtual environment and install test
dependencies before running tests (optional):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if present
```

## Usage

Run the CLI script under `bin/` with the `parse` subcommand to analyze a
log file. Basic usage:

```bash
python bin/advanced_traffic_analyzer.py parse --filepath PATH [options]
```

Options:

- `--filepath`, `-f` : Path to the log file (required)
- `--method`         : Filter by HTTP method (GET, POST, PUT, DELETE, ...)
- `--status`         : Filter by HTTP status or status range (e.g. 200 or 200-299)
- `--start`          : Start timestamp (inclusive)
- `--end`            : End timestamp (inclusive)
- `--top`            : Number of top results to show (default depends on CLI)

Example:

```bash
python bin/advanced_traffic_analyzer.py parse --filepath tests/test_logs.log --top 5
```

## Project structure

- `bin/` - CLI entrypoint(s).
- `internal/` - core implementation: analyzers, entity models, utilities and
	view/formatting code.
- `tests/` - unit tests and test fixtures.

The code separates concerns into `entity` (data models), the analysis core
(`anazyler`), and `view` (presentation). This keeps parsing, aggregation, and
output formatting independent and easier to test.

## Development and testing

Run the test suite with `pytest` from the repository root:

```bash
pytest -q
```

If you modify code, consider running the tests and linters (if configured).

## Limitations and potential improvements

- Improve the `view` module to support multiple output formats (JSON, CSV).
- Add configuration for additional aggregations and time-binning.
- Harden log parsing for more formats and graceful handling of corrupted
	lines.
- Add a small CI configuration to run tests automatically.

Contributions, bug reports and documentation improvements are welcome.