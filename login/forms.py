from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur ou email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

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
    roll_number = forms.CharField(
        max_length=20,
        required=False,
        label="Numéro d'étudiant",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['user_type', 'roll_number']