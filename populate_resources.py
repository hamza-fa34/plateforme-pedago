import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from teacherhome.models import Resource
from django.contrib.auth.models import User
from login.models import UserProfile
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

# --- Nettoyage des anciennes ressources ---
Resource.objects.all().delete()
print("Toutes les anciennes ressources ont été supprimées.")

# Paramètres de génération
N = 50  # Nombre de ressources à créer
subjects = ['IT', 'Développement Web', 'Développement Mobile', 'Gestion de projet', 'Data Science', 'Cybersécurité', 'Cloud', 'DevOps']
levels = ['L1', 'L2', 'L3', 'M1', 'M2', 'Master', 'Pro', 'Certification']
types = ['Cours', 'TD', 'TP', 'Examen', 'Projet', 'Tutoriel', 'Workshop', 'Documentation']
exts = ['pdf', 'doc', 'ppt', 'txt', 'md', 'zip']

# Récupérer tous les enseignants existants
teachers = list(User.objects.filter(userprofile__user_type='teacher'))
if not teachers:
    print("Aucun enseignant trouvé.")
    exit()

os.makedirs('media/resources', exist_ok=True)

# --- Création des utilisateurs enseignants ---
for i in range(1, 11):
    username = f"teacher{i}"
    email = f"teacher{i}@gmail.com"
    password = "Azerty123@"
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
            }
        )
        user.email = email  # Toujours mettre à jour l'email
        user.set_password(password)  # Toujours mettre à jour le mot de passe
        user.save()
        if created or not hasattr(user, 'userprofile'):
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'user_type': 'teacher'}
            )
        print(f"Enseignant créé : {username} / {email}")
    except IntegrityError:
        print(f"Erreur lors de la création de l'enseignant : {username}")

# --- Création des utilisateurs étudiants ---
for i in range(1, 51):
    username = f"student{i}"
    email = f"student{i}@gmail.com"
    password = "Azerty123@"
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
            }
        )
        user.email = email  # Toujours mettre à jour l'email
        user.set_password(password)  # Toujours mettre à jour le mot de passe
        user.save()
        if created or not hasattr(user, 'userprofile'):
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'user_type': 'student', 'roll_number': f"RN{i:03d}"}
            )
        print(f"Étudiant créé : {username} / {email}")
    except IntegrityError:
        print(f"Erreur lors de la création de l'étudiant : {username}")

# --- Création des ressources par des profs aléatoires ---
for i in range(N):
    subject = random.choice(subjects)
    level = random.choice(levels)
    rtype = random.choice(types)
    ext = random.choice(exts)
    title = f"Ressource {i+1} - {subject} - {level} - {rtype}"
    fake_file_name = f"fake_{i+1}.{ext}"
    file_path = f"media/resources/{fake_file_name}"
    # Créer un fichier factice si besoin
    with open(file_path, "w") as f:
        f.write(f"Ceci est un fichier factice pour test : {title}\n")
    # Choisir un enseignant au hasard
    owner = random.choice(teachers)
    # Créer la ressource
    Resource.objects.create(
        owner=owner,
        title=title,
        subject=subject,
        level=level,
        resource_type=rtype,
        file=f"resources/{fake_file_name}",
        permission=1,  # public
        keywords=[subject, rtype, level]
    )
    print(f"Ajouté : {title} (par {owner.username})")

print("Population terminée !") 