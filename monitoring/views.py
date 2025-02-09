# monitoring/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.gis.geos import Point  # Import Point from GeoDjango
import logging

# Import models and forms
from .models import CustomUser, Farmer, Field, Sensor, CropType, Pest, CropHealthIssue, FertilizerApplication, IrrigationSchedule, WeatherData, SensorData
from .forms import CustomUserCreationForm, UserLoginForm, FarmerProfileForm

# Set up logging
logger = logging.getLogger(__name__)

def register(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if it's a validation-only request
            if request.POST.get('validation_only'):
                return JsonResponse({'success': True})
            
            # Actual user creation
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            logger.info(f"New user registered: {user.email}")

            # Return JSON response for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/login/'})
            
            messages.success(request, "Registration successful! Welcome!")
            return redirect('login')
        else:
            logger.error(f"Registration failed: {form.errors}")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            
            return render(request, 'register.html', {'form': form})

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to login page

@login_required
def farmer_profile(request):
    """
    Handles farmer profile updates.
    """
    farmer = Farmer.objects.get(user_id=request.user.id)
    user = CustomUser.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('farmer_profile')
    else:
        form = FarmerProfileForm(instance=farmer)
    
    return render(request, 'farmer_profile.html', {
        'farmer': farmer, 'form': form, "user": user})

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        remember_me = request.POST.get('remember_me', False)

        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)

                # Set session expiry based on "Remember Me"
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session

                messages.success(request, "Login successful. Welcome back!")
                return redirect('dashboard')  # Redirect to the dashboard

        messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def home_view(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html')

def test_messages(request):
    """
    Test view to demonstrate different types of messages.
    """
    messages.success(request, "This is a success message.")
    messages.info(request, "This is an info message.")
    messages.warning(request, "This is a warning message.")
    messages.error(request, "This is an error message.")

    return render(request, 'test_messages.html')

def example_view(request):
    """
    Example view to demonstrate messages.
    """
    messages.success(request, "Operation was successful!")
    messages.error(request, "Something went wrong. Please try again.")
    return render(request, 'example.html')

@login_required
def SetupField_view(request):
    """
    Renders the field setup page.
    """
    fields = Field.objects.filter(farmer=request.user.farmer)
    crop_types = CropType.objects.all()
    return render(request, 'setupField.html', {
        'fields': fields,
        'crop_types': crop_types
    })

def create_field(request):
    """
    Handles the creation of a new field.
    """
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_size = request.POST.get('field_size')
        crop_type_id = request.POST.get('crop_type')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Validate latitude and longitude
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            messages.error(request, 'Invalid latitude or longitude.')
            return redirect('SetupField')

        # Create a Point object for the location
        location = Point(longitude, latitude, srid=4326)  # SRID 4326 is for WGS84 (standard for GPS)

        # Get the logged-in farmer
        farmer = request.user.farmer

        # Save to database
        Field.objects.create(
            farmer=farmer,
            name=field_name,
            size=field_size,
            crop_type_id=crop_type_id,
            location=location  # Add the location field
        )
        messages.success(request, 'Field created successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def add_sensor(request):
    """
    Handles the addition of a new sensor.
    """
    if request.method == 'POST':
        sensor_type = request.POST.get('sensor_type')
        unit = request.POST.get('unit')
        field_id = request.POST.get('field')

        # Save to database
        Sensor.objects.create(
            field_id=field_id,
            sensor_type=sensor_type,
            unit=unit
        )
        messages.success(request, 'Sensor added successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def add_crop_type(request):
    """
    Handles the addition of a new crop type.
    """
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        description = request.POST.get('description')

        # Save to database
        CropType.objects.create(
            name=crop_name,
            description=description
        )
        messages.success(request, 'Crop type added successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def record_pest(request):
    """
    Handles the recording of a new pest.
    """
    if request.method == 'POST':
        pest_name = request.POST.get('pest_name')
        description = request.POST.get('description')
        severity_level = request.POST.get('severity_level')
        image = request.FILES.get('image')
        crop_types = request.POST.getlist('crop_types')

        # Save the pest
        pest = Pest.objects.create(
            name=pest_name,
            description=description,
            severity_level=severity_level,
            image=image
        )

        # Add affected crop types
        pest.crop_types.set(crop_types)
        messages.success(request, 'Pest recorded successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def record_health_issue(request):
    """
    Handles the recording of a new crop health issue.
    """
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        field_id = request.POST.get('field')

        # Save to database
        CropHealthIssue.objects.create(
            field_id=field_id,
            issue_type=issue_type,
            description=description,
            image=image
        )
        messages.success(request, 'Crop health issue recorded successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def add_fertilizer(request):
    """
    Handles the addition of a new fertilizer application.
    """
    if request.method == 'POST':
        fertilizer_type = request.POST.get('fertilizer_type')
        amount = request.POST.get('amount')
        field_id = request.POST.get('field')
        date = request.POST.get('date')  # Get the date value

        # Save to database
        FertilizerApplication.objects.create(
            field_id=field_id,
            date=date,  # Save the provided date
            fertilizer_type=fertilizer_type,
            amount=amount
        )
        messages.success(request, 'Fertilizer added successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

def add_irrigation(request):
    """
    Handles the addition of a new irrigation schedule.
    """
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        interval = request.POST.get('interval')
        field_id = request.POST.get('field')

        # Save to database
        IrrigationSchedule.objects.create(
            field_id=field_id,
            start_time=start_time,
            end_time=end_time,
            interval=interval
        )
        messages.success(request, 'Irrigation added successfully!')
        return redirect('SetupField')
    
    return redirect('SetupField')

@login_required
def dashboard_view(request):
    """
    Renders the dashboard with field, weather, and sensor data.
    """
    # Fetch fields for the logged-in farmer
    fields = Field.objects.filter(farmer=request.user.farmer)

    # Add latest weather data to each field
    for field in fields:
        #field.weather_data = WeatherData.objects.filter(field=field).order_by('-timestamp').first()
        # Current weather data
        field.current_weather = WeatherData.objects.filter(field=field, is_forecast=False).order_by('-timestamp').first()

        # Forecast data (next 5 days, 8 intervals/day)
        field.forecast_weather = WeatherData.objects.filter(field=field, is_forecast=True).order_by('timestamp')[:40]
    
     # Recent sensor data
        field.sensor_data = SensorData.objects.filter(sensor__field=field).order_by('-timestamp')[:10]

        # Recent crop health issues
        field.crop_health_issues = CropHealthIssue.objects.filter(field=field).order_by('-issue_type')[:10]

        # Active irrigation schedules
        field.irrigation_schedules = IrrigationSchedule.objects.filter(field=field)

    context = {
        'fields': fields,
        # Add other context data if needed
    }
    return render(request, 'dashboard.html', context)