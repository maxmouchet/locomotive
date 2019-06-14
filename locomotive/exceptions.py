import click


class PassengerNotFoundException(click.ClickException):
    def __init__(self, passenger: str) -> None:
        super().__init__("Passenger {} not found".format(passenger))


class StationNotFoundException(click.ClickException):
    def __init__(self, station: str) -> None:
        super().__init__("Train station for {} not found".format(station))
