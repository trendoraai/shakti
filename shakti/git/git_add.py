import click
import subprocess


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def git_add(args):
    """Run black and then git add with given arguments."""
    click.echo("Running black...")
    try:
        subprocess.run(["poetry", "run", "black", "."], check=True)
        click.echo("Black formatting complete.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running black: {e}")
        return

    click.echo("Adding files to staging area with arguments: " + " ".join(args))
    try:
        subprocess.run(["git", "add"] + list(args), check=True)
        click.echo("Files added to staging area.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error adding files: {e}")
