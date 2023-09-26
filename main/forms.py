from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import AccountInformation, LandInformation, STRSForestInformation, LocalLevel, Ward


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local_level'].queryset = LocalLevel.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()
        
        if 'local_level' in self.data:
            try:
                local_level_id = int(self.data.get('local_level'))
                self.fields['ward'].queryset = Ward.objects.filter(local_level_id = local_level_id).order_by('name')
            except:
                pass
        elif self.instance.pk:
            self.fields['ward'].queryset = Ward.objects.filter(local_level_id=self.instance.local_level_id).order_by('name')



        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['local_level'].queryset = LocalLevel.objects.filter(province_id = province_id).order_by('name')
            except:
                pass
        elif self.instance.pk:
            self.fields['local_level'].queryset = LocalLevel.objects.filter(province_id=self.instance.province_id).order_by('name')

        
        


class STRSForestInformationForm(forms.ModelForm):
    class Meta:
        model = STRSForestInformation
        fields = ('tree_species', 'tree_type', 'tree_code', 'plantation_year', 'girth_cm', 'average_height')
