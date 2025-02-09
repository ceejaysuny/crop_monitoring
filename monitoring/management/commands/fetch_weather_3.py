import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import Field, WeatherData  # Changed from your_app to monitoring

class Command(BaseCommand):
    help = 'Fetches weather data for all fields and saves it to the database'

    def handle(self, *args, **kwargs):
        API_KEY = '2d67fde302e0f93a7f31731e7a6190a5'  # Replace with actual API key
        if not API_KEY:
            self.stdout.write(self.style.ERROR('Missing OpenWeatherMap API key'))
            return

        BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

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

                response = requests.get(BASE_URL, params=params)
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch data for {field.name}: {response.status_code}'))
                    continue

                data = response.json()
                weather_data = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'precipitation': data.get('rain', {}).get('1h', 0)
                }

                WeatherData.objects.create(
                    field=field,
                    timestamp=timezone.now(),
                    **weather_data
                )
                self.stdout.write(self.style.SUCCESS(f'Updated weather for {field.name}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))