# :train2: sncf-cli

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/sncf-cli.svg)](https://pypi.org/project/sncf-cli/)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/yafeunteun/sncf-cli.svg)](https://codeclimate.com/github/yafeunteun/sncf-cli/maintainability)
[![Build Status](https://travis-ci.org/yafeunteun/sncf-cli.svg?branch=master)](https://travis-ci.org/yafeunteun/sncf-cli)
[![Coverage Status](https://coveralls.io/repos/github/yafeunteun/sncf-cli/badge.svg?branch=master&service=github)](https://coveralls.io/github/yafeunteun/sncf-cli?branch=master)

You love SNCF. You love command line tools. sncf-cli is made for you !

<img src="https://raw.githubusercontent.com/yafeunteun/sncf-cli/master/assets/carbon.png">

## Installation

`sncf-cli` requires Python 3.6+ and can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install sncf-cli
```

## Usage

sncf-cli is easy to use. Find below simple examples:

```bash
# RTFM bro (just kidding)
sncf-cli search --help
# Search by city name
sncf-cli search Amsterdam Paris
# Search by train station code (Amsterdam to Paris here)
sncf-cli search NLAMA FRPAR
# Pick a date and even a travel class B-)
sncf-cli search Brest Paris --date 2019/07/14 --class first 
```

**PRO TIP** By default, results are formatted to look simple. Consequently it filters many information you might want to have access. Use the following option to get the complete JSON API response:
 ```bash
sncf-cli search Brest Paris --date 2019/07/14 --formatter raw
```

## Development

```bash
pip install -e .[dev]

black locomotive  # Code formatter
mypy locomotive   # Type checking
pylint locomotive # Linter
pytest            # Unit tests
```

```bash
# Cleanup (use with care !)
git clean -dfx
```

```
assets/      # Images used in the README
locomotive/  # Python module (see locomotive/README.md)
tests/       # Unit tests
```

### Releases

```bash
git tag vX.Y.Z # e.g. v0.4.0
git push --tags
```

**Checklist:**

- [ ] Screenshot in README is up to date.

### Design notes & future plans

Currently the `Formatter`s are tightly coupled with the API response format. In the future we may implement an abstraction over different APIs versions.

We use `attrs` instead of `@dataclass` for Python 3.6 compatibility.

## Licenses

sncf-cli is released under the [MIT license](https://github.com/yafeunteun/sncf-cli/blob/master/LICENSE).  
The train stations database (`stations-lite.csv`) is derived from `stations.csv` ([trainline-eu/stations](https://github.com/trainline-eu/stations)) released under the Open Database License (ODbL) license.
