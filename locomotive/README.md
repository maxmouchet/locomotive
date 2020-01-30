# locomotive module

## Code structure

```bash
api/               # Clients for SNCF APIs
api/oui_v3.py      # Client for the wshoraires.oui.sncf v3 API

cli/               # CLI (locomotive)
cli/__init__.py    # CLI entrypoint
cli/commands/      # CLI commands (search, ...)
cli/formatters.py  # Output formatters
cli/templates/     # Output formatters templates

data/              # Data files (train stations database, ...)
models/            # Data models shared between modules (Passenger, Station, ...)
stores/            # Stores for data models
```
