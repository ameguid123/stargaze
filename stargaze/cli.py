"""
stargaze

Usage:
  stargaze visible
  stargaze -h | --help
  stargaze --version

Options:
  -h --help                 Show this screen.
  --version                 Show version.

Examples:
  stargaze visible

Help:
  For help, please see the Github repository:
  https://github.com/ameguid123/stargaze
"""

from docopt import docopt
from inspect import getmembers, isclass
from . import __version__ as VERSION
from colorama import init

# Framework credit to:
# https://stormpath.com/blog/building-simple-cli-interfaces-in-python


def main():
    """CLI entrypoint"""
    from colorama import init
    init()
    import stargaze.commands
    options = docopt(__doc__, version=VERSION)
    for key, val in options.items():
        module = getattr(stargaze.commands, key, None)
        if module and val:
            cmds = getmembers(module, isclass)
            # cmd[1] is the class, cmd[0] is the class name
            # CommandTemplate is in the respective module b/c inheritance
            cmd = [cmd[1] for cmd in cmds if cmd[0] != 'CommandTemplate'][0]
            cmd = cmd(options)
            cmd.run()
