from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
    )
    
    NIVEAU_CHOICES = (
        ('', 'Sélectionnez votre niveau'),
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    )
    
    FILIERE_CHOICES = (
        ('', 'Sélectionnez votre filière'),
        ('informatique', 'Informatique'),
        ('mathematiques', 'Mathématiques'),
        ('physique', 'Physique'),
        ('chimie', 'Chimie'),
        ('biologie', 'Biologie'),
    )

    MATIERE_CHOICES = (
        ('mathematiques', 'Mathématiques'),
        ('physique', 'Physique'),
        ('informatique', 'Informatique'),
        ('chimie', 'Chimie'),
        ('biologie', 'Biologie'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name="Type d'utilisateur")
    
    # Champs pour les étudiants
    roll_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro d'étudiant")
    niveau = models.CharField(max_length=2, choices=NIVEAU_CHOICES, blank=True, null=True, verbose_name="Niveau d'études")
    filiere = models.CharField(max_length=20, choices=FILIERE_CHOICES, blank=True, null=True, verbose_name="Filière")
    
    # Champs pour les enseignants
    matricule = models.CharField(max_length=20, blank=True, null=True, verbose_name="Matricule enseignant")
    matieres_enseignees = models.JSONField(default=list, blank=True, verbose_name="Matières enseignées")

    def __str__(self):
        return self.user.username