import click

from ..passengers import Passenger


@click.group()
def passengers(**args):
    pass


@passengers.command()
@click.pass_context
def add(ctx, **args):
    # TODO: Handle name conflicts
    name = click.prompt("Name")
    age = click.prompt("Age")
    passenger = Passenger(age=age, name=name)
