"""
CLI command for managing passenger profiles.
"""

import datetime as dt

from attr import NOTHING

import click
import dateparser as dp

from ...models.passenger import Passenger


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
    attrs = {}
    # TODO: Move this generic logic outside
    for attr in Passenger.__attrs_attrs__:
        text = attr.name.replace("_", " ").capitalize()
        default = None
        value_proc = None
        if attr.default != NOTHING:
            default = attr.default
        if attr.type is dt.date:
            value_proc = dp.parse
        attrs[attr.name] = click.prompt(text, default=default, value_proc=value_proc)
    passenger = Passenger(**attrs)
    passengers_.add(passenger)
    passengers_.save()
    click.echo("Passenger saved to {}".format(passengers.path))


@passengers.command()
@click.pass_context
def show(ctx):
    """
    Show passengers profiles.
    """
    passengers_ = ctx.obj["passengers"]
    for passenger in passengers_:
        click.echo(passenger)
