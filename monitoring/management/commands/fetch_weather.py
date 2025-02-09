import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import Field, WeatherData
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetches weather data and forecast for all fields and saves it to the database'

    def handle(self, *args, **kwargs):
        API_KEY = settings.WEATHER_API_KEY  # Replace with actual API key
        if not API_KEY:
            self.stdout.write(self.style.ERROR('Missing OpenWeatherMap API key'))
            return

        CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
        FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'

        try:
            for field in Field.objects.all():
                if not field.location:
                    continue
                lat, lon = field.location.y, field.location.x
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': API_KEY,
                    'units': 'metric'
                }

                # Fetch current weather data
                response_current = requests.get(CURRENT_WEATHER_URL, params=params)
                if response_current.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch current data for {field.name}: {response_current.status_code}'))
                else:
                    data_current = response_current.json()
                    weather_data_current = {
                        'temperature': data_current['main']['temp'],
                        'humidity': data_current['main']['humidity'],
                        'precipitation': data_current.get('rain', {}).get('1h', 0),
                        'is_forecast': False,  # Mark as current weather data
                    }
                    WeatherData.objects.create(
                        field=field,
                        timestamp=timezone.now(),
                        **weather_data_current
                    )
                    self.stdout.write(self.style.SUCCESS(f'Updated current weather for {field.name}'))

                # Fetch forecast data
                response_forecast = requests.get(FORECAST_URL, params=params)
                if response_forecast.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch forecast data for {field.name}: {response_forecast.status_code}'))
                else:
                    forecast_data = response_forecast.json().get('list', [])
                    for entry in forecast_data:
                        weather_data_forecast = {
                            'temperature': entry['main']['temp'],
                            'humidity': entry['main']['humidity'],
                            'precipitation': entry.get('rain', {}).get('3h', 0),
                            'timestamp': timezone.make_aware(timezone.datetime.fromisoformat(entry['dt_txt'])),
                            'is_forecast': True,  # Mark as forecast data
                        }
                        WeatherData.objects.create(field=field, **weather_data_forecast)
                    self.stdout.write(self.style.SUCCESS(f'Updated forecast for {field.name}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))