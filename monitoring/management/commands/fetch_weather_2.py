import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import Field, WeatherData

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches weather data for all fields and saves it to the database'

    def handle(self, *args, **kwargs):
        try:
            # API endpoint and key
            API_KEY = '2d67fde302e0f93a7f31731e7a6190a5'
            BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

            # Fetch weather data for each field
            for field in Field.objects.all():
                lat, lon = field.location.y, field.location.x  # Get latitude and longitude from PointField
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': API_KEY,
                    'units': 'metric'  # Use metric units (Celsius, mm, etc.)
                }

                # Make API request
                response = requests.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()

                    # Extract relevant weather data
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    precipitation = data.get('rain', {}).get('1h', 0)  # Precipitation in the last hour

                    # Save to WeatherData model
                    WeatherData.objects.create(
                        field=field,
                        timestamp=timezone.now(),
                        temperature=temperature,
                        humidity=humidity,
                        precipitation=precipitation
                    )
                    logger.info(f'Successfully fetched weather data for {field.name}')
                else:
                    logger.error(f'Failed to fetch weather data for {field.name}: {response.status_code}')
        except Exception as e:
            logger.error(f'An error occurred: {str(e)}')