# :train2: sncf-cli

[![Python Version](https://img.shields.io/badge/python-3-blue.svg?style=flat)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/yafeunteun/sncf-cli/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/yafeunteun/sncf-cli.svg?branch=master)](https://travis-ci.org/yafeunteun/sncf-cli)

## TODO

- [ ] Travis-CI
- [ ] Coverage
- [ ] PyPI push (https://docs.travis-ci.com/user/deployment/pypi/, + badge)
- [ ] Improve README (screenshot, https://carbon.now.sh/)

## Usage

```bash
pip install sncf-cli
sncf-cli search --help
```

```bash
sncf-cli search FRBES FRPAR
```

## Development

```bash
pip install -e .
pip install black pylint pytest-cov
black locomotive
pylint locomotive
coverage run --source locomotive/ -m pytest
```
