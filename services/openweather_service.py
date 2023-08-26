from typing import Optional, Tuple
import os

from dotenv import load_dotenv
import httpx

from infrastructure import weather_cache
from models.validation_error import ValidationError
from constants.abbriviations import COUNTRY_CODES, US_STATES_CODES

load_dotenv()

API_KEY =os.getenv('OPENWEATHERMAP_API_KEY', default='no-key')

class ValidationError(Exception):
    def __init__(self, error_message: str, status_code: int):
        super().__init__(error_message)
        self.error_message = error_message
        self.status_code = status_code

async def get_report_async(
        city,
        state: Optional[str],
        country: str,
        units: str) -> dict:
    

    if forcast := weather_cache.get_weather(city, state, country, units):
        return forcast

    # if forcast := redis.hset('key')
    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'
    
    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    url =f'{api_url}?q={q}&appid={API_KEY}&units={units}'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise ValidationError(response.text, response.status_code)

    data = response.json()
    forcast = data['main']

    weather_cache.set_weather(city, state, country, units, forcast)
    return forcast

def validate_units(city: str,
                   state: Optional[str],
                   country: Optional[str],
                   units: Optional[str]) -> Tuple[str, Optional[str], str, Optional[str]]:

    city = city.strip().lower()
    if not country:
        country = 'US'
    else:
        country = country.strip().upper()
    
    if country not in COUNTRY_CODES:
        error = f'invalid country: {country}. It must be a two letter abbreviation such as US or GB.'
        raise ValidationError(error_message=error, status_code=400)
    
    if state: 
        state = state.upper().strip()
    
    if state not in US_STATES_CODES:
        error = f'Invalid state: {state}. It must be a two letter abbreviatoon such as CA or NY(US only).'
        raise ValidationError(error_message=error, status_code=400)
    
    if units:
        units = units.lower().strip()
    
    validate_units = ('statard', 'metric', 'imperial')
    if units not in validate_units:
        error = f'invalid units:{units}, it must be one of {validate_units}'
        raise ValidationError(error_message=error, status_code=400)
    
    return city, state, country, units
