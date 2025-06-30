from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur ou email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur ou email",
            'aria-label': "Nom d'utilisateur ou email"
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre mot de passe",
            'aria-label': "Mot de passe"
        })
    )

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Créez un mot de passe",
            'aria-label': "Mot de passe"
        }),
        label="Mot de passe"
    )
    first_name = forms.CharField(
        label="Nom complet",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre nom complet",
            'aria-label': "Nom complet"
        })
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Votre adresse email",
            'aria-label': "Adresse email"
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'aria-label': "Type d'utilisateur"
        }),
        label="Vous êtes"
    )
    roll_number = forms.CharField(
        max_length=20,
        required=False,
        label="Numéro d'étudiant",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Numéro d'étudiant (si étudiant)",
            'aria-label': "Numéro d'étudiant"
        })
    )

    class Meta:
        model = UserProfile
        fields = ['user_type', 'roll_number']