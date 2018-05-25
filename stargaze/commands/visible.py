from .command_template import CommandTemplate
import ephem
import math
from colorama import Fore
from datetime import datetime


class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        usr = CommandTemplate.usr
        deg_to_rad = 180.0 / math.pi
        sun = ephem.Sun()
        sun.compute(usr)
        sun_angle = sun.alt * deg_to_rad
        sun_status = Fore.RED
        # Civil/nautical twilight
        if sun_angle <= -6:
            sun_status = Fore.YELLOW
            # Astronomical twilight
            if sun_angle <= -18:
                sun_status = Fore.GREEN

        for obj, ephem_obj in self.objects.items():
            alt_symbol = '↓'
            # Object is rising
            if usr.next_antitransit(ephem_obj) > usr.next_transit(ephem_obj):
                alt_symbol = '↑'
            # NOTE: needs to come after rising/setting calculation
            ephem_obj.compute(usr)
            info_str = ('%8s: altitude: %5.1f deg %s, azimuth: %5.1f deg'
                        % (obj, ephem_obj.alt * deg_to_rad, alt_symbol,
                            ephem_obj.az * deg_to_rad))
            if sun_status == Fore.RED:
                print(sun_status + info_str + ', sun\'s still up')
            elif ephem_obj.alt * deg_to_rad < 0:
                print(Fore.RED + info_str + ', object beneath horizon')
            elif sun_status == Fore.YELLOW:
                print(sun_status + info_str +
                      ', viewing may be difficult during twilight')
            else:
                print(sun_status + info_str + ', good viewing conditions!')
