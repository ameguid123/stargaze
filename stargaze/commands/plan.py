from .command_template import CommandTemplate
import ephem
from colorama import Fore
import math


class Plan(CommandTemplate):
    """List view time information for celestial objects from user's location"""
    def run(self):
        usr = CommandTemplate.usr

        for obj, ephem_obj in self.objects.items():
            self.print_status(obj, ephem_obj)
            # Planet moons don't have attribute for rising/setting
            try:
                next_rise = usr.next_rising(ephem_obj)
                next_set = usr.next_setting(ephem_obj)
            except AttributeError:
                continue

            # TODO: Potentially better way than these strftimes
            if next_rise > next_set:
                print(Fore.WHITE + '\tObject setting at %s'
                      % ephem.localtime(next_set).strftime("%m-%d %H:%M:%S"))
                print('\tObject rising at %s'
                      % ephem.localtime(next_rise).strftime("%m-%d %H:%M:%S"))
            else:
                print(Fore.WHITE + '\tObject rising at %s'
                      % ephem.localtime(next_rise).strftime("%m-%d %H:%M:%S"))
                print('\tObject setting at %s'
                      % ephem.localtime(next_set).strftime("%m-%d %H:%M:%S"))
