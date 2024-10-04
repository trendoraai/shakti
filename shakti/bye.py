import click


@click.command()
def bye():
    """A simple program that says goodbye."""
    click.echo("Goodbye from Shakti!")
