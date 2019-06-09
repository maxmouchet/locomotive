import click

from ..passengers import Passenger


@click.group()
def passengers(**args):
    pass


@passengers.command()
@click.pass_context
def add(ctx, **args):
    passengers = ctx.obj["passengers"]
    # TODO: Handle name conflicts
    name = click.prompt("Name")
    age = click.prompt("Age", type=int)
    passenger = Passenger(age=age, name=name)
    passengers.add(passenger)
    passengers.save()


@passengers.command()
@click.pass_context
def show(ctx, **args):
    passengers = ctx.obj["passengers"]
    for passenger in passengers:
        click.echo(passenger)
