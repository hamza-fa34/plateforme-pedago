from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Type d'utilisateur"
    )
    filiere = forms.ChoiceField(
        choices=[('', 'Sélectionnez votre filière')] + list(UserProfile.FILIERE_CHOICES),
        required=False,
        label="Filière"
    )
    niveau = forms.ChoiceField(
        choices=[('', 'Sélectionnez votre niveau')] + list(UserProfile.NIVEAU_CHOICES),
        required=False,
        label="Niveau d'études"
    )
    roll_number = forms.CharField(
        max_length=20,
        required=False,
        label="Numéro d'étudiant"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                filiere=self.cleaned_data.get('filiere', ''),
                niveau=self.cleaned_data.get('niveau', ''),
                roll_number=self.cleaned_data.get('roll_number', '')
            )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['user_type', 'filiere', 'niveau', 'roll_number']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Initialiser les champs utilisateur
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
        
        # Rendre les champs facultatifs si l'utilisateur est un enseignant
        if self.instance and self.instance.user_type == 'teacher':
            self.fields['filiere'].required = False
            self.fields['niveau'].required = False
            self.fields['roll_number'].required = False
    
    def save(self, commit=True):
        # Mettre à jour les champs utilisateur
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        
        # Sauvegarder le profil
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile