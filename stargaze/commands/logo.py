from .command_template import CommandTemplate


class Logo(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        with open('logo.txt', 'r') as f:
            print(f.read(), end="")
