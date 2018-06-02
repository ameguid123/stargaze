import json
import requests
import ephem
import math
from colorama import Fore
from datetime import datetime
from string import capwords
import dateparser
import pytz
from tzlocal import get_localzone as localtz
import pickle
import os
from os.path import expanduser, isfile
from collections import OrderedDict
import inquirer
from ast import literal_eval
import sys

CACHE_FILE = os.path.dirname(os.path.realpath(__file__)) + '/.location_cache'

# TODO: MAJOR need to migrate to new geoip format by July 1st, 2018
# TODO: manual specification of latlon+better file cleanup than garbage collect


def get_location(specifyCustomLoc):
    """Get user's latitude and longitude using freegeoip.net. If offline,
       allows user to select from previous 10 locations used or specify a
       custom location with a latitude and longitude"""
    if isfile(CACHE_FILE):
        location_cache = pickle.load(open(CACHE_FILE, 'rb'))
    else:
        location_cache = OrderedDict()

    if specifyCustomLoc:
        return (choose_location(list(location_cache.items())[:10]))

    try:
        req = (requests.get('http://freegeoip.net/json'))
        loc = json.loads(req.text)
        latlon = (str(loc['latitude']), str(loc['longitude']))
        key = ','.join(latlon)
        if key not in location_cache:
            location_cache[key] = loc
            pickle.dump(location_cache, open(CACHE_FILE, 'wb'))
    # TODO: specific except
    except:
        return (choose_location(list(location_cache.items())[:10]))
    return latlon


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


def choose_location(option_list):
    options = ['{0}, {1} ({2}, {3})'.format(
                                            elem[1]['city'],
                                            elem[1]['region_name'],
                                            elem[1]['latitude'],
                                            elem[1]['longitude']
                                            )
               for elem in option_list]
    questions = [
        inquirer.List(
            'location',
            message='Choose location or enter custom location',
            choices=options + ['custom']
        ),
    ]
    answers = inquirer.prompt(questions)
    loc = (answers['location'])
    if loc == 'custom':
        loc = input('Enter custom location as: `(latitude, longitude)`:\n')
    try:
        latlon = literal_eval((loc[loc.find("("):loc.find(")") + 1]))
        return (str(latlon[0]), str(latlon[1]))
    except (SyntaxError, ValueError):
        print('ERROR: Invalid custom location entry')
        sys.exit(1)


class CommandTemplate:
    """Template from which all commands will inherit"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.usr = create_observer(get_location(options['-l']))
        self.objects = {}
        usr, objects = self.usr, self.objects

        # Build user's custom set of objects
        if options['OBJECTS']:
            build_objects(options['OBJECTS'], objects, usr)

        else:
            # Default objects are solar system planets
            for candidate in ephem._libastro.builtin_planets():
                if candidate[1] == 'Planet' and candidate[2] != 'Sun':
                    objects[candidate[2]] = getattr(ephem, candidate[2])(usr)

        # Change user's date if specified
        if options['-t']:
            try:
                local_dt = localtz().localize(dateparser.parse(options['-t']))
                print('Time set to: ' + local_dt.strftime('%Y-%m-%d %H:%M:%S'))
                usr.date = local_dt.astimezone(pytz.utc)
            except:
                print('Could not interpret date, using local time')

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
