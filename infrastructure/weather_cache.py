from datetime import datetime, timedelta
from typing import Optional, Tuple

__cache = {}

lifetime_in_hours = 1.0

def __clean_out_of_data():
    for key, data in __cache.items():
        dt = datetime.now() - data.get('time')
        if dt / timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]


def set_weather(city: str,
            state: Optional[str],
            country: str,
            units: str,
            value: dict) -> Optional[dict]:
    
    key = __create_key(city, state, country, units)
    data = {
        'time': datetime.now(),
        'value': value, 

    }
    __cache[key] = data
    __clean_out_of_data() 

def __create_key(city: str, state: str, country: str, units: str) -> Tuple[str, str , str, str]:
    if not city or not country or not units:
        raise Exception('City, country and units are required')

    if not state:
        state = ''

    return city.strip().lower(), state.strip().lower(), country.strip().lower(), units.strip().lower()

def get_weather(
        city: str,
        state: Optional[str],
        country: str,
        units: str,) -> Optional[dict]: 
    key = __create_key(city, state, country, units)
    data = __cache.get(key)

    if not data: 
        return None
    
    last = data.get('time')
    dt = datetime.now() - last
    if dt / timedelta(minutes = 60) < lifetime_in_hours:
        return data.get('value')
    
    del __cache[key]
    return None

# lage cache    
# lage en funksjon som henter data from openweather
## denne funksjonen skal ta inn en location og units 
## Lager data i cache
## returnere data

## hvis data fins, sjekk holdbarhet og returner data
## hvis holdbarhet er gått ut, slett data fra cache 

# lag en funksjon som lagrer data 
## denne funksjonen skal ta inn data of en location
## lagre data i cache med timestamp

# kanskje en clean cache funklsjon som sletter data som er for gammel 