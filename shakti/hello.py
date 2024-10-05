from shakti.utils import register_command


@register_command
def hello(args):
    """A simple program that says hello."""
    print("Hello from Shakti!")
