# crop_monitoring

The Crop Monitoring App is a Django-based application designed to help farmers monitor and manage their crops effectively. The app provides features for managing fields, sensors, weather data, pest detection, crop health issues, fertilizer applications, and irrigation schedules.

## Features

- User Management: Custom user model with registration and authentication.
- Field Management: Create and manage fields with precise location tracking using GeoDjango.
- Sensor Management: Add and manage sensors for monitoring various parameters.
- Weather Data: Fetch and store weather data for fields.
- Pest Detection: Record and manage detected pests.
- Crop Health Issues: Record and manage crop health issues.
- Fertilizer Application: Manage fertilizer applications.
- Irrigation Schedule: Manage irrigation schedules.
- Notifications: Send notifications to users.

## Installation

GDAL: Geospatial Data Abstraction Library is required for this project

Read more here (https://pypi.org/project/GDAL/)

GDAL can be quite complex to build and install, particularly on Windows and MacOS. Pre built binaries are provided for the conda system:

I suggest you install conda, create virtual environment with conda. You can easily install GDAL on conda virtual environment.

Please read more here
https://pypi.org/project/GDAL/

https://docs.conda.io/en/latest/

https://conda-forge.org/


Database that support PostGIS is required for this project.
I suggest installing Postgress Database, it support PostGIS

Read more here

https://www.youtube.com/watch?v=EkQ9c8bUNIk


1. **Clone the repository**:
    ```sh
    git clone https://github.com/ceejaysuny/crop_monitoring.git
    cd crop_monitoring
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt

    ```

    **Set up environment variables:**

   Create a `.env` file in the root directory of your project and add your WeatherAPI.com API key:

   
   WEATHER_API_KEY=your_api_key_here
   ```

4. **Set up the database**:
    - Update the database settings in [settings.py](http://_vscodecontentref_/0).
    - Run migrations:
        ```sh
        python manage.py migrate
        ```

5. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Access the application**:
    Open your web browser and go to [http://127.0.0.1:8000](http://_vscodecontentref_/1).

2. **Register and log in**:
    Register a new user or log in with the superuser credentials.

3. **Manage fields**:
    - Navigate to the field management section to create and manage fields.
    - Add sensors to fields for monitoring various parameters.

4. **Fetch weather data**:
    - Use the management command to fetch weather data:
        ```sh
        python manage.py fetch_weather
        You can create script to fetch_weather.py automatically
       
        ```

5. **Record pests and crop health issues**:
    - Navigate to the pest detection and crop health issue sections to record and manage data.

6. **Manage fertilizer applications and irrigation schedules**:
    - Navigate to the respective sections to manage fertilizer applications and irrigation schedules.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [GeoDjango](https://docs.djangoproject.com/en/stable/ref/contrib/gis/)
- [OpenWeatherMap](https://openweathermap.org/)

## Contact

For any inquiries, please contact ekejimbe@gmail.com.