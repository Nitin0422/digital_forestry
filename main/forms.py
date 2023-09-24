from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import AccountInformation, LandInformation


User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))


class AccountInformationForm(forms.ModelForm):
    class Meta:
        model = AccountInformation
        fields = ("full_name", "address", "phone_number", "PAN")

class LandInformationForm(forms.ModelForm):
    class Meta:
        model = LandInformation
        fields = ('province', 'local_level', 'ward', 'kitta_number', 'area', 'gps_latitude', 'gps_longitude', 'is_greater_than_10Ha')

