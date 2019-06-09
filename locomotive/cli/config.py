import click
import json


@click.group()
def config(**args):
    pass


@config.command()
@click.pass_context
def init(ctx, **args):
    """
    Initialize the configuration file.

    \b
    To create a configuration file in specific location:
    sncf-cli --config-file /mydir/config.json config init
    """
    path = ctx.obj["config"].init()
    click.echo("Initialized configuration file at {}".format(path))


@config.command()
@click.pass_context
def show(ctx, **args):
    click.echo(json.dumps(ctx.obj["config"].config, indent=2))
