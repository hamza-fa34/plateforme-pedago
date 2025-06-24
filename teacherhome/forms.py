# forms.py
from django import forms
from .models import Resource

class FileModelForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['file', 'permission']