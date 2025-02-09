"""
URL configuration for crop_monitoring project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from . import views
from .views import (
    register, logout_view, farmer_profile, SetupField_view,
    create_field, add_sensor, add_crop_type, record_pest,
    record_health_issue, add_fertilizer, add_irrigation
)

urlpatterns = [
    # Root path
    path('', views.home_view, name='home'),

    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Farmer profile and field setup URLs
    path('farmer_profile/', farmer_profile, name='farmer_profile'),
    path('SetupField/', SetupField_view, name='SetupField'),

    # Field management URLs
    path('create-field/', create_field, name='create_field'),
    path('add-sensor/', add_sensor, name='add_sensor'),
    path('add-crop-type/', add_crop_type, name='add_crop_type'),
    path('record-pest/', record_pest, name='record_pest'),
    path('record-health-issue/', record_health_issue, name='record_health_issue'),
    path('add-fertilizer/', add_fertilizer, name='add_fertilizer'),
    path('add-irrigation/', add_irrigation, name='add_irrigation'),

    # Dashboard and testing URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test-messages/', views.test_messages, name='test_messages'),

    # Captcha URLs
    path('captcha/', include('captcha.urls')),

    # Admin URL (optional, if you're using Django admin)
    #path('admin/', admin.site.urls),
]