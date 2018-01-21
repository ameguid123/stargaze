from .command_template import CommandTemplate
import ephem
import math
from colorama import Fore
import time


class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        deg_to_rad = 180.0 / math.pi
        sun = ephem.Sun()
        sun.compute(CommandTemplate.usr)
        sun_angle = sun.alt * deg_to_rad
        sun_status = Fore.RED
        # alt_symbol = '↓'
        # Civil/nautical twilight
        if sun_angle <= -6:
            sun_status = Fore.YELLOW
            # Astronomical twilight
            if sun_angle <= -18:
                sun_status = Fore.GREEN
        # TODO: Replace self.planets with a dict to avoid cumbersome getattr?
        for planet in self.planets:
            obj = getattr(ephem, planet)(CommandTemplate.usr)
            # if CommandTemplate.usr.next_antitransit(obj) > CommandTemplate.usr.next_transit(obj):
            #     alt_symbol = '↑'
            info_str = ('%8s: altitude: %5.1f deg, azimuth: %5.1f deg'
                        % (planet, obj.alt * deg_to_rad,  # alt_symbol,
                           obj.az * deg_to_rad))
            if sun_status == Fore.RED:
                print(sun_status + info_str + ', sun\'s still up')
            elif obj.alt * deg_to_rad < 0:
                print(Fore.RED + info_str + ', planet beneath horizon')
            elif sun_status == Fore.YELLOW:
                print(sun_status + info_str +
                      ', viewing may be difficult during twilight')
            else:
                print(sun_status + info_str + ', good viewing conditions!')
