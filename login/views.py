from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
            profile.save()

            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login(request):
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
                    return render(request, 'index.html', {
                        'form': form,
                        'error_message': "Aucun profil utilisateur associé à ce compte. Contactez l'administrateur."
                    })
            else:
                return render(request, 'index.html', {
                    'form': form,
                    'error_message': 'Identifiants invalides.'
                })
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})

def forgot_password(request):
    return redirect('login')

def logout(request):
    auth_logout(request)
    return redirect('login')