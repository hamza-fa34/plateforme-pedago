from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, UserProfileForm, LoginForm

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = user_form.cleaned_data['first_name']
            if profile_form.cleaned_data['user_type'] == 'student':
                profile.roll_number = profile_form.cleaned_data['roll_number']
                profile.niveau = profile_form.cleaned_data.get('niveau', '')
                profile.filiere = profile_form.cleaned_data.get('filiere', '')
            profile.save()

            messages.success(request, 'Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.')
            return redirect('login')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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