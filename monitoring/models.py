from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a superuser with all permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No username required

    def __str__(self):
        return self.email



class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    ) 
    address = models.CharField(max_length=255, blank=True) 

class CropType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class Field(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=255)
    location = PointField(srid=4326) # SRID 4326 for WGS84  # Using GeoDjango's PointField for precise location tracking
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,  help_text="Size in hectares") 
    crop_type = models.ForeignKey(CropType, on_delete=models.SET_NULL, null=True, blank=True, help_text="Current crop planted in this field")
    #farm_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Moved farm_size here
    def __str__(self):
        return self.name 

class Sensor(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=50) 
    unit = models.CharField(max_length=10) 

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
'''
class WeatherData(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
'''

class WeatherData(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()  # This will represent the forecasted timestamp
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    is_forecast = models.BooleanField(default=False)  # Indicates if this is a forecast




class Pest(models.Model):    
    name = models.CharField(max_length=255)
    description = models.TextField()
    severity_level = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='pest_images/')
    crop_types = models.ManyToManyField(CropType, blank=True)

class CropHealthIssue(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=255)  
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True) 

class FertilizerApplication(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    date = models.DateField()
    fertilizer_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class IrrigationSchedule(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.IntegerField()  # e.g., interval in days

class Notification(models.Model):
    INFO = 'Info'
    WARNING = 'Warning'
    ALERT = 'Alert'
    CATEGORY_CHOICES = [
        (INFO, 'Information'),
        (WARNING, 'Warning'),
        (ALERT, 'Alert'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=INFO)
    is_read = models.BooleanField(default=False)

