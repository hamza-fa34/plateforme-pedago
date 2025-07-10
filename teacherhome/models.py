from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Resource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    title = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)  # Matière
    level = models.CharField(max_length=100, blank=True, null=True)    # Niveau
    resource_type = models.CharField(max_length=50, blank=True, null=True)  # Type (cours, TD, etc.)
    file = models.FileField(upload_to='resources/')
    permission = models.IntegerField(choices=[(0, 'Privé'), (1, 'Public')])
    keywords = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)

    def __str__(self):
        return f"{self.owner.username}'s Resource: {self.file.name}"

class ResourceView(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} viewed {self.resource.file.name}"