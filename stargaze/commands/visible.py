from .command_template import CommandTemplate
import ephem
import math
from colorama import Fore


class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        deg_to_rad = 180.0 / math.pi
        sun = ephem.Sun()
        sun.compute(CommandTemplate.usr)
        sun_angle = sun.alt * deg_to_rad
        sun_status = Fore.RED
        # Civil twilight
        if sun_angle <= -6:
            sun_status = Fore.YELLOW
            # Nautical twilight
            if sun_angle <= -12:
                # Astronomical twilight
                if sun_angle <= -18:
                    sun_status = Fore.GREEN
        for planet in self.planets:
            obj = getattr(ephem, planet)(CommandTemplate.usr)
            info_str = ('%s: altitude: %4.1f deg, azimuth: %5.1f deg'
                        % (planet, obj.alt * deg_to_rad, obj.az * deg_to_rad))
            if sun_status == Fore.RED:
                print(sun_status + info_str + ', sun\'s still up')
            elif obj.alt * deg_to_rad < 0:
                print(Fore.RED + info_str + ', planet beneath horizon')
            else:
                print(sun_status + info_str)
