import json
import requests
import ephem
import math
from colorama import Fore
from datetime import datetime
from string import capwords


def get_location():
    """Get user's latitude and longitude using freegeoip.net"""
    req = (requests.get('http://freegeoip.net/json'))
    loc = json.loads(req.text)
    return (str(loc['latitude']), str(loc['longitude']))


def create_observer(usr_coords):
    """Create PyEphem observer using user latitude/longitude and UTC time"""
    usr = ephem.Observer()
    usr.lat, usr.lon = usr_coords
    usr.date = datetime.utcnow()
    return usr


# NOTE: returns the time in UTC (as for all PyEphem functions)
def sun_test(obs):
    """Sun's altitude/azimuth and rise/noon/set time for PyEphem observer"""
    sun = ephem.Sun()
    sun.compute(obs)
    print('sun altitude: %s, sun azimuth: %s' % (sun.alt, sun.az))
    print('sun rise time: %s' % obs.previous_rising(sun))
    print('solar noon: %s ' % obs.next_transit(sun))
    print('sunset time: %s' % obs.next_setting(sun))


def build_objects(candidates, objects, usr):
    """Modify `objects` dict to contain PyEphem entry corresponding to
        `candidates` keys"""
    for candidate in candidates:
        candidate = capwords(candidate.lower())
        try:
            objects[candidate] = getattr(ephem, candidate)(usr)
        except AttributeError:
            pass


class CommandTemplate:
    """Template from which all commands will inherit"""
    usr = create_observer(get_location())

    objects = {}

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        usr, objects = self.usr, self.objects

        # Build user's custom set of objects
        if options['OBJECTS']:
            build_objects(options['OBJECTS'], objects, usr)

        else:
            # Default objects are solar system planets
            for candidate in ephem._libastro.builtin_planets():
                if candidate[1] == 'Planet' and candidate[2] != 'Sun':
                    objects[candidate[2]] = getattr(ephem, candidate[2])(usr)

    def run(self):
        raise NotImplementedError('This command has not been implemented!')

    def print_status(self, obj, ephem_obj):
        """Given a celestial object name `obj` and the PyEphem object
        representing it `ephem_obj` produce relevant status printout"""
        usr = self.usr
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
