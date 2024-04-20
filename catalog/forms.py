from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    house_number = forms.CharField(max_length=255)
    street_name = forms.CharField(max_length=255)
    town_city = forms.CharField(max_length=255)
    county = forms.CharField(max_length=255)
    eir_code = forms.CharField(max_length=7)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('house_number', 'street_name', 'town_city', 'county', 'eir_code',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user_profile = UserProfile(user=user, house_number=self.cleaned_data['house_number'], street_name=self.cleaned_data['street_name'], town_city=self.cleaned_data['town_city'], county=self.cleaned_data['county'], eir_code=self.cleaned_data['eir_code'])
        if commit:
            user.save()
            user_profile.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
    house_number = forms.CharField(max_length=255)
    street_name = forms.CharField(max_length=255)
    town_city = forms.CharField(max_length=255)
    county = forms.CharField(max_length=255)
    eir_code = forms.CharField(max_length=7)

    class Meta:
        model = UserProfile
        fields = ['house_number', 'street_name', 'town_city', 'county', 'eir_code']

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.house_number = self.cleaned_data['house_number']
        user_profile.street_name = self.cleaned_data['street_name']
        user_profile.town_city = self.cleaned_data['town_city']
        user_profile.county = self.cleaned_data['county']
        user_profile.eir_code = self.cleaned_data['eir_code']
        if commit:
            user_profile.save()
        return user_profile