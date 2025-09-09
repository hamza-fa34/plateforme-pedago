from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, ProfileUpdateForm, LoginForm, UserRegisterForm

def signup(request):
    if request.method == 'POST':
        # Créer un dictionnaire avec les données du formulaire
        form_data = request.POST.copy()
        
        # Créer le formulaire avec les données du POST
        form = UserRegisterForm(form_data)
        
        if form.is_valid():
            # Sauvegarder l'utilisateur et créer le profil
            user = form.save(commit=True)
            
            # Connecter automatiquement l'utilisateur après l'inscription
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            
            if user is not None:
                auth_login(request, user)
                
                # Rediriger en fonction du type d'utilisateur
                if user.userprofile.user_type == 'student':
                    return redirect('studenthome')
                else:
                    return redirect('teacher_home')
            
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')
        else:
            # Afficher les erreurs de formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}" if field in form.fields else error)
    else:
        form = UserRegisterForm()

    # Préparer les données pour le template
    context = {
        'form': form,
        'user_form': form,
        'profile_form': form
    }
    
    return render(request, 'signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                try:
                    user_profile = user.userprofile
                    if user_profile.user_type == 'student':
                        return redirect('studenthome')
                    elif user_profile.user_type == 'teacher':
                        return redirect('teacher_home')
                    else:
                        return redirect('no_access')
                except UserProfile.DoesNotExist:
                    messages.error(request, "Aucun profil utilisateur associé à ce compte. Contactez l'administrateur.")
                    return render(request, 'index.html', {'form': form})
            else:
                messages.error(request, 'Identifiants invalides.')
                return render(request, 'index.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Veuillez entrer votre adresse email.")
        else:
            # Pour des raisons de sécurité, on affiche le même message que l'email existe ou non
            messages.info(request, "Si un compte est associé à cet email, un lien de réinitialisation a été envoyé.")
        return redirect('forgot_password')
    return render(request, 'forgot_password.html')

def logout(request):
    auth_logout(request)
    return redirect('login')