import click


class StationNotFoundException(click.ClickException):
    def __init__(self, station: str) -> None:
        super().__init__("Train station for {} not found".format(station))
