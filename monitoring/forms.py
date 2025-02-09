# file: app/forms.py
from django.contrib.auth.forms import AuthenticationForm

# monitoring/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)  # Create user but don't save yet
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()  # Save the user object
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'}),
        label='Password'
    )
    #captcha = CaptchaField()  # Add CAPTCHA field for security
    #captcha = CaptchaField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data

    def get_user(self):
        return self.user

# forms.py
from .models import Farmer

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'pattern': r'\+?[0-9]{1,3}[0-9]{10,15}',
                'title': 'Enter valid phone number with country code (e.g., +234XXXXXXXXXX) (10-15 digits)'
            }),
            'address': forms.Textarea(attrs={'rows': 3})
        }
