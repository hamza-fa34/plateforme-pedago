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
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre adresse email',
            'aria-label': 'Adresse email'
        })
    )
    first_name = forms.CharField(
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
            'aria-label': 'Prénom'
        })
    )
    last_name = forms.CharField(
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom',
            'aria-label': 'Nom'
        })
    )
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'radio-option'
        }),
        label="Type d'utilisateur",
        required=True
    )
    
    # Champs pour les étudiants
    roll_number = forms.CharField(
        required=False,
        label="Numéro d'étudiant",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control student-field'})
    )
    
    niveau = forms.ChoiceField(
        choices=UserProfile.NIVEAU_CHOICES,
        required=False,
        label="Niveau d'études",
        widget=forms.Select(attrs={'class': 'form-control student-field'})
    )
    
    filiere = forms.ChoiceField(
        choices=UserProfile.FILIERE_CHOICES,
        required=False,
        label="Filière",
        widget=forms.Select(attrs={'class': 'form-control student-field'})
    )
    
    # Champs pour les enseignants
    matricule = forms.CharField(
        required=False,
        label="Matricule enseignant",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control teacher-field'})
    )
    
    matieres = forms.MultipleChoiceField(
        choices=UserProfile.MATIERE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'teacher-field'}),
        label="Matières enseignées"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'student':
            if not cleaned_data.get('roll_number'):
                self.add_error('roll_number', 'Ce champ est obligatoire pour les étudiants')
            if not cleaned_data.get('niveau'):
                self.add_error('niveau', 'Veuillez sélectionner votre niveau')
            if not cleaned_data.get('filiere'):
                self.add_error('filiere', 'Veuillez sélectionner votre filière')
        elif user_type == 'teacher':
            if not cleaned_data.get('matricule'):
                self.add_error('matricule', 'Le matricule est obligatoire')
            if not cleaned_data.get('matieres'):
                self.add_error('matieres', 'Veuillez sélectionner au moins une matière')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Créer ou mettre à jour le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_type = self.cleaned_data['user_type']
            
            if self.cleaned_data['user_type'] == 'student':
                profile.roll_number = self.cleaned_data['roll_number']
                profile.niveau = self.cleaned_data['niveau']
                profile.filiere = self.cleaned_data['filiere']
                profile.matricule = ''
                profile.matieres_enseignees = []
            else:  # Enseignant
                profile.matricule = self.cleaned_data['matricule']
                profile.matieres_enseignees = self.cleaned_data['matieres']
                profile.roll_number = ''
                profile.niveau = ''
                profile.filiere = ''
                
            profile.save()
            
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