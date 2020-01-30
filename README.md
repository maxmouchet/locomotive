<p align="center">
  <img src="/docs/_assets/logo.png" height="150"><br/>
  <i>Python API clients and a CLI for France's railways :sparkles:</i><br/><br/>
  <a href="https://codeclimate.com/github/yafeunteun/sncf-cli/maintainability">
    <img src="https://img.shields.io/codeclimate/maintainability/yafeunteun/sncf-cli.svg">
  </a>
  <a href="https://github.com/yafeunteun/sncf-cli/actions">
    <img src="https://github.com/yafeunteun/sncf-cli/workflows/CI/badge.svg">
  </a>
  <a href="https://coveralls.io/github/yafeunteun/sncf-cli?branch=master">
    <img src="https://coveralls.io/repos/github/yafeunteun/sncf-cli/badge.svg?branch=master&service=github">
  </a>
</p>

<img src="/docs/_assets/carbon.png">

## Installation

`sncf-cli` requires Python 3.6+ and can be installed using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install sncf-cli
```

## API Clients

Module | Features | Status
-------|----------|-------
[oui_v3](/locomotive/api/oui_v3.py) | Travel Request | ![oui_v3](https://github.com/yafeunteun/sncf-cli/workflows/oui_v3/badge.svg)

## CLI

sncf-cli is easy to use. Find below simple examples:

```bash
sncf-cli search --help
# Search by city name
sncf-cli search Amsterdam Paris
# Search by train station code (Amsterdam to Paris here)
sncf-cli search NLAMA FRPAR
# Pick a date and even a travel class
sncf-cli search Brest Paris --date 2019/07/14 --class first
```

## Development

```bash
poetry install
poetry run sncf-cli

# pre-commit
poetry run pre-commit install
poetry run pre-commit run --all-files
```

```
assets/      # Images used in the README
locomotive/  # Python module (see locomotive/README.md)
tests/       # Unit tests
```

### Releases

```bash
poetry version X.Y.Z # e.g. v0.4.0
git tag vX.Y.Z
git push --tags
```

**Checklist:**

- [ ] Screenshot in README is up to date.
- [ ] Set version in `pyproject.toml`

### Design notes & future plans

Currently the `Formatter`s are tightly coupled with the API response format. In the future we may implement an abstraction over different APIs versions.

We use `attrs` instead of `@dataclass` for Python 3.6 compatibility.

## Licenses

sncf-cli is released under the [MIT license](https://github.com/yafeunteun/sncf-cli/blob/master/LICENSE).
The train stations database (`stations-lite.csv`) is derived from `stations.csv` ([trainline-eu/stations](https://github.com/trainline-eu/stations)) released under the Open Database License (ODbL) license.

*Logo: Train Tickets by b farias from the Noun Project.*
