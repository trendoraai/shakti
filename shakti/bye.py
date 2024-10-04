import click


@click.command(help="Say goodbye from Shakti")
def bye():
    """A simple program that says goodbye."""
    click.echo("Goodbye from Shakti!")
