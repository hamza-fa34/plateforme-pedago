from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .forms import UserForm, UserProfileForm

def login(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

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
            # Le nom est maintenant dans le User model (first_name)
            profile.name = user_form.cleaned_data['first_name']
            profile.save()

            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            try:
                user_profile = user.userprofile
                if user_profile.user_type == 'student':
                    return redirect('studenthome')
                elif user_profile.user_type == 'teacher':
                    return redirect('teacherhome')
                else:
                    # Fallback au cas où le profil n'a pas de rôle valide
                    return redirect('no_access')
            except UserProfile.DoesNotExist:
                # Gérer le cas où un User n'a pas de UserProfile (ex: superuser)
                return redirect('no_access')
        else:
            # L'authentification a échoué
            return render(request, 'index.html', {'error_message': 'Identifiants invalides.'})

    return render(request, 'index.html')

def forgot_password(request):
    # Logique de réinitialisation de mot de passe à implémenter
    # Pour l'instant, redirige simplement vers la page de connexion
    # avec un message (qui peut être affiché dans le template)
    return redirect('login') # Ajout d'un message serait une bonne amélioration

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from urllib.parse import unquote
def forgot_password(request):
    login_email = request.GET.get('email')
    print("Login Email:", login_email)
    email = login_email
    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        print("No User")
        return render(request, 'index.html', {'error_message': 'No account found with this email address'})
    forgot_value = user_profile.forgot
    name = user_profile.name
    
    forgotPasswordMail(email, forgot_value,name)
    print("Mail Sent")
    return render(request, 'index.html')

def forgotPasswordMail(to_email,password,name = "User"):
    MAIL_ID = "ENTER_YOUR_GMAIL"
    # Refer this to create app password : https://support.google.com/accounts/answer/185833?hl=en
    PASSWORD = "xxxx xxxx xxxx xxxx"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    subject = "Password Recovery - Academia Campus Repository"
    msg = MIMEMultipart()
    msg['From'] = MAIL_ID
    msg['To'] = to_email
    msg['Subject'] = subject
    
    content = """
                <p>Dear NAME,</p>
                <p>Your Password is : <b> PASSWORD </b></p>
                <br>
                <p><b>With Regards,</b></p>
                <br>
                <img src="cid:image1" alt="Image" style="width: 250px;">
                """.replace("PASSWORD",password).replace("NAME",name)
    msg.attach(MIMEText(content, 'html'))
    
    with open("textLogo.png", 'rb') as image_file:
        img = MIMEImage(image_file.read(), name='image.png')
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(MAIL_ID, PASSWORD)
        server.sendmail(MAIL_ID, to_email, msg.as_string())