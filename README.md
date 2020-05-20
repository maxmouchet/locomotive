<p align="center">
  <img src="/docs/_assets/logo.png" height="150"><br/>
  <i>Python API clients and a CLI for France's railways :sparkles:</i><br/><br/>
  <a href="https://maxmouchet.github.io/locomotive">
    <img src="https://img.shields.io/badge/docs-master-blue.svg?style=flat">
  </a>
  <a href="https://github.com/maxmouchet/locomotive/actions">
    <img src="https://github.com/maxmouchet/locomotive/workflows/CI/badge.svg">
  </a>
  <a href="https://coveralls.io/github/maxmouchet/locomotive?branch=master">
    <img src="https://coveralls.io/repos/github/maxmouchet/locomotive/badge.svg?branch=master&service=github">
  </a>
</p>

<img src="/docs/_assets/carbon.png">

## Installation

`locomotive` requires Python 3.6+ and can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install locomotive
```

## API Clients

Module | Features | Status
-------|----------|-------
[oui_v3](/locomotive/api/oui_v3.py) | Travel Request | ![oui_v3](https://github.com/maxmouchet/locomotive/workflows/oui_v3/badge.svg)
[gc](/locomotive/api/gc.py) | Board Request | ![oui_v3](https://github.com/maxmouchet/locomotive/workflows/gc/badge.svg)

## CLI

locomotive is easy to use. Find below simple examples:

```bash
locomotive search --help
# Search by city name
locomotive search Amsterdam Paris
# Search by train station code (Amsterdam to Paris here)
locomotive search NLAMA FRPAR
# Pick a date and even a travel class
locomotive search Brest Paris --date 2019/07/14 --class first
```

## Development

```bash
poetry install
poetry run locomotive

# pre-commit
poetry run pre-commit install
poetry run pre-commit run --all-files
```

### Releases

```bash
poetry version X.Y.Z # e.g. v0.4.0
git tag vX.Y.Z
git push --tags
```

## Licenses

locomotive is released under the [MIT license](https://github.com/maxmouchet/locomotive/blob/master/LICENSE).
The train stations database (`stations-lite.csv`) is derived from `stations.csv` ([trainline-eu/stations](https://github.com/trainline-eu/stations)) released under the Open Database License (ODbL) license.

*Logo: Train Tickets by b farias from the Noun Project.*
