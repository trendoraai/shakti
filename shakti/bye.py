from shakti.utils import register_command


@register_command
def bye(args):
    """A simple program that says goodbye."""
    print("Goodbye from Shakti!")
