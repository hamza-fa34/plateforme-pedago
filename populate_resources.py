import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from teacherhome.models import Resource
from django.contrib.auth.models import User

# Paramètres de génération
N = 50  # Nombre de ressources à créer
subjects = ['Math', 'Physique', 'Chimie', 'SVT', 'Histoire', 'Géo', 'Anglais']
levels = ['L1', 'L2', 'L3', 'M1', 'M2', 'Terminale']
types = ['Cours', 'TD', 'TP', 'Examen', 'Projet']
exts = ['pdf', 'doc', 'ppt', 'txt']

# Récupérer un enseignant existant
teacher = User.objects.filter(userprofile__user_type='teacher').first()
if not teacher:
    print("Aucun enseignant trouvé.")
    exit()

os.makedirs('media/resources', exist_ok=True)

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
    # Créer la ressource
    Resource.objects.create(
        owner=teacher,
        title=title,
        subject=subject,
        level=level,
        resource_type=rtype,
        file=f"resources/{fake_file_name}",
        permission=1,  # public
        keywords=[subject, rtype, level]
    )
    print(f"Ajouté : {title}")

print("Population terminée !") 