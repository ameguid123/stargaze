from .command_template import CommandTemplate


class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        print('Visible:')
