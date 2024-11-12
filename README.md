# Mushpedia Scraper

[![Continous Integration](https://github.com/cmnemoi/mushpedia_scraper/actions/workflows/ci.yaml/badge.svg)](https://github.com/cmnemoi/mushpedia_scraper/actions/workflows/ci.yaml) 
[![Continous Integration](https://github.com/cmnemoi/mushpedia_scraper/actions/workflows/publish_to_pypi.yaml/badge.svg)](https://github.com/cmnemoi/mushpedia_scraper/actions/workflows/publish_to_pypi.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/mushpedia_scraper/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/mushpedia_scraper)
[![PyPI version](https://badge.fury.io/py/mushpedia-scraper.svg)](https://badge.fury.io/py/mushpedia-scraper)

Scraper for https://mushpedia.com/

# Usage

Install with `python -m pip install --user mushpedia-scraper`

Then run `python mushpedia-scraper` in your terminal. For the moment, the raw HTML pages are printed to the terminal.

# Contributing

You need to have `curl` and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed on your system.

Then run the following command : `curl -sSL https://raw.githubusercontent.com/cmnemoi/mushpedia_scraper/main/clone-and-install | bash`

## Development

Run tests with `make test`.

# License

The source code of this repository is licensed under the [MIT License](LICENSE).