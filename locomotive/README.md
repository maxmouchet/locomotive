# locomotive module

## Code structure

```
api/               # Clients for SNCF APIs
api/oui_v1/        # Client for the oui.sncf/proposition/rest/search-travels/outward API
api/oui_v2/        # Client for the oui.sncf/wishes-api/wishes API

cli/               # CLI tool (sncf-cli)
cli/__init__.py    # CLI entrypoint
cli/commands/      # CLI commands (search, ...)
cli/formatters.py  # Output formatters
cli/templates/     # Output formatters templates

data/              # Data files (train stations database, ...)
models/            # Data models shared between modules (Passenger, Station, ...)
```
