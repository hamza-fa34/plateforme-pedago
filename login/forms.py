from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    first_name = forms.CharField(label="Nom complet")

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Vous êtes"
    )

    class Meta:
        model = UserProfile
        fields = ['user_type']