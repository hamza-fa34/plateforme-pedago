from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    roll_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro d'étudiant")

    def __str__(self):
        return self.user.username