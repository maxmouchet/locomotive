"""
CLI command for managing passenger profiles.
"""

import click

from ...models.passengers import Passenger


@click.group()
def passengers():
    """
    Manage passenger profiles.
    """


@passengers.command()
@click.pass_context
def add(ctx):
    """
    Add a passenger profile.
    """
    passengers_ = ctx.obj["passengers"]
    # TODO: Handle name conflicts
    name = click.prompt("Name")
    age = click.prompt("Age", type=int)
    passenger = Passenger(age=age, name=name)
    passengers_.add(passenger)
    passengers_.save()


@passengers.command()
@click.pass_context
def show(ctx):
    """
    Show passengers profiles.
    """
    passengers_ = ctx.obj["passengers"]
    for passenger in passengers_:
        click.echo(passenger)
