from .command_template import CommandTemplate
import ephem
import math
class Visible(CommandTemplate):
    """List celestial objects visible from the user's location"""
    def run(self):
        deg_per_rad = 180.0 / math.pi
        for planet in self.planets:
            obj = getattr(ephem, planet)(CommandTemplate.usr)
            print("%s: altitude: %4.1f deg, azimuth: %5.1f deg" 
                     % (planet, obj.alt * deg_per_rad, obj.az * deg_per_rad))
