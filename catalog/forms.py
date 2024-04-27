from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import models, UserProfile 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    house_number = forms.CharField(max_length=255)
    street_name = forms.CharField(max_length=255)
    town_city = forms.CharField(max_length=255)
    county = forms.CharField(max_length=255)
    eir_code = forms.CharField(max_length=7)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'house_number', 'street_name', 'town_city', 'county', 'eir_code',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user_profile = UserProfile(user=user, house_number=self.cleaned_data['house_number'], street_name=self.cleaned_data['street_name'], town_city=self.cleaned_data['town_city'], county=self.cleaned_data['county'], eir_code=self.cleaned_data['eir_code'])
        if commit:
            user.save()
            user_profile.save()
        return user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['house_number', 'street_name', 'town_city', 'county', 'eir_code']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class MessageForm(forms.Form):
    your_name = forms.CharField(max_length=100)
    your_message = forms.CharField(widget=forms.Textarea)

class Message(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()