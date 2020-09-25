import click


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass
