# :train2: sncf-cli

[![Python Version](https://img.shields.io/badge/python-3-blue.svg?style=flat)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/sncf-cli.svg)](https://pypi.org/project/sncf-cli/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/yafeunteun/sncf-cli/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/yafeunteun/sncf-cli.svg?branch=master)](https://travis-ci.org/yafeunteun/sncf-cli)
[![Coverage Status](https://coveralls.io/repos/github/yafeunteun/sncf-cli/badge.svg?branch=master)](https://coveralls.io/github/yafeunteun/sncf-cli?branch=master)

<img src="/assets/carbon.png">

## TODO

- [ ] PyPI push (https://docs.travis-ci.com/user/deployment/pypi/, + badge)
- [ ] Improve README
- [ ] Test on Windows

## Installation

```bash
pip install sncf-cli
```

## Usage

```bash
sncf-cli search --help
sncf-cli search Amsterdam Paris
sncf-cli search FRBES FRPAR
```

## Development

```bash
pip install -e .
pip install black mypy pylint pytest-cov

black locomotive  # Code formatter
mypy locomotive   # Type checking
pylint locomotive # Linter
pytest            # Unit tests
```

## Licenses

sncf-cli is released under the [MIT license](https://github.com/yafeunteun/sncf-cli/blob/master/LICENSE).  
The train stations database (`stations-lite.csv`) is derived from `stations.csv` ([trainline-eu/stations](https://github.com/trainline-eu/stations)) released under the Open Database License (ODbL) license.
