from .command_template import CommandTemplate
import ephem
import math
from colorama import Fore
from datetime import datetime


class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        for obj, ephem_obj in self.objects.items():
            self.print_status(obj, ephem_obj)
