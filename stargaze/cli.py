import json
import requests
import ephem
from datetime import datetime
def main():
    usr = create_observer(get_location())
    sun_test(usr)

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

def sun_test(obs):
    """Sun's altitude/azimuth and rise/noon/set time for PyEphem observer"""
    sun = ephem.Sun()
    sun.compute(obs)
    print("sun altitude: %s, sun azimuth: %s" % (sun.alt, sun.az))
    print("sun rise time: %s" % obs.previous_rising(sun))
    print("solar noon: %s "% obs.next_transit(sun))
    print("sunset time: %s" % obs.next_setting(sun))
 
if __name__ == "__main__":
    main()
