# forms.py
from django import forms
from .models import Resource

class FileModelForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        help_text="Séparez les mots-clés par des virgules"
    )
    
    class Meta:
        model = Resource
        fields = ['title', 'subject', 'level', 'resource_type', 'file', 'permission']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.txt,.odt'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser le champ keywords avec les valeurs existantes
        if self.instance and self.instance.keywords:
            self.initial['keywords'] = ', '.join(self.instance.keywords)
    
    def clean(self):
        cleaned_data = super().clean()
        # Vérifier que le fichier est présent
        if 'file' not in self.files:
            raise forms.ValidationError("Un fichier doit être fourni.")
        return cleaned_data
    
    def save(self, commit=True):
        # Convertir la chaîne de mots-clés en liste
        keywords = self.cleaned_data.get('keywords', '')
        if keywords:
            self.instance.keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Sauvegarder l'instance
        instance = super().save(commit=False)
        
        # Si c'est une nouvelle instance, on doit sauvegarder d'abord pour obtenir un ID
        if commit and not instance.pk:
            instance.save()
            self.save_m2m()
        elif commit:
            instance.save()
            
        return instance