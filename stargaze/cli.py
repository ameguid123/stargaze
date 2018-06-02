"""
stargaze

Usage:
  stargaze visible [-l] [-t TIME] [OBJECTS ...]
  stargaze plan [-l] OBJECTS ...
  stargaze -h | --help
  stargaze --version

Arguments:
  OBJECTS                   Celestial objects you're interested in.

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  -t TIME                   Specify a viewing time.
  -l                        Specify a location.

Examples:
  stargaze visible
  stargaze visible mars jupiter saturn europa
  stargaze visible -t "tomorrow at 11pm" neptune uranus pluto
  stargaze plan venus mercury
  stargaze plan -l saturn jupiter

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
