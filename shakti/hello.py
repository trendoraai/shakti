import click


@click.command()
def hello():
    """A simple program that says hello."""
    click.echo("Hello from Shakti!")
