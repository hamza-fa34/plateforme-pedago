from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
import os

from login.models import UserProfile
from .models import Resource, ResourceView

User = get_user_model()

class ResourceModelTests(TestCase):
    def setUp(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.contrib.auth import get_user_model
        import os
        from django.conf import settings
        
        User = get_user_model()
        
        # Créer un utilisateur enseignant
        self.teacher = User.objects.create_user(
            username='prof_test',
            email='prof@test.com',
            password='testpass123'
        )
        
        # Créer un répertoire temporaire pour les fichiers de test
        self.test_media_dir = os.path.join(settings.BASE_DIR, 'test_media')
        os.makedirs(self.test_media_dir, exist_ok=True)
        
        # Créer un fichier de test
        self.test_file_path = os.path.join(self.test_media_dir, 'test_file.txt')
        with open(self.test_file_path, 'wb') as f:
            f.write(b'Contenu du fichier de test')
        
        # Créer un fichier téléchargeable
        self.test_file = SimpleUploadedFile(
            name='test_file.txt',
            content=open(self.test_file_path, 'rb').read(),
            content_type='text/plain'
        )
        
        # Créer une ressource avec des mots-clés
        self.resource = Resource(
            owner=self.teacher,
            email='prof@test.com',
            title='Cours avancé de Django',
            subject='Informatique',
            level='M2',
            resource_type='cours',
            file=self.test_file,
            permission=1  # Public
        )
        # Définir les mots-clés après la création de l'instance
        self.resource.keywords = ['django', 'web']
        self.resource.save()
        
        # Rafraîchir l'instance pour s'assurer que les données sont à jour
        self.resource.refresh_from_db()
    
    def test_resource_creation(self):
        """Test la création d'une ressource"""
        # Créer une nouvelle ressource pour le test
        test_file = SimpleUploadedFile(
            'test_file.txt',
            b'file_content',
            content_type='text/plain'
        )
        
        resource = Resource.objects.create(
            owner=self.teacher,
            email='test@example.com',
            title='Test Resource',
            subject='Test Subject',
            level='L1',
            resource_type='cours',
            file=test_file,
            permission=1,  # Public
            keywords=['test', 'resource']
        )
        
        # Vérifier les champs de base
        self.assertEqual(str(resource), f"{self.teacher.username}'s Resource: {resource.file.name}")
        self.assertEqual(resource.title, 'Test Resource')
        self.assertEqual(resource.subject, 'Test Subject')
        self.assertEqual(resource.level, 'L1')
        self.assertEqual(resource.resource_type, 'cours')
        self.assertEqual(resource.permission, 1)  # Public
        
        # Vérifier que les mots-clés sont correctement enregistrés
        self.assertIsNotNone(resource.keywords, "Les mots-clés ne devraient pas être None")
        self.assertIsInstance(resource.keywords, (list, type(None)), "Les mots-clés devraient être une liste ou None")
        
        # Convertir en liste si c'est une chaîne
        if isinstance(resource.keywords, str):
            keywords = [k.strip() for k in resource.keywords.split(',') if k.strip()]
        else:
            keywords = resource.keywords or []
            
        # Vérifier le contenu des mots-clés
        self.assertCountEqual(keywords, ['test', 'resource'], 
                            f"Les mots-clés devraient être ['test', 'resource'], mais sont {keywords}")
        
        self.assertTrue(self.resource.file)
    
    def test_resource_view_creation(self):
        """Test la création d'une vue de ressource"""
        # Créer un étudiant qui va voir la ressource
        student = User.objects.create_user(
            username='etudiant_test',
            email='etudiant@test.com',
            password='testpass123'
        )
        
        # Créer une vue de ressource
        resource_view = ResourceView.objects.create(
            resource=self.resource,
            user=student
        )
        
        self.assertEqual(str(resource_view), f"{student.username} viewed {self.resource.file.name}")
        self.assertEqual(self.resource.views.count(), 1)
        self.assertEqual(self.resource.views.first().user, student)


class TeacherHomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Créer un enseignant
        self.teacher = User.objects.create_user(
            username='prof_test',
            email='prof@test.com',
            password='testpass123',
            first_name='Professeur',
            last_name='Test'
        )
        
        # Créer un profil pour l'enseignant
        UserProfile.objects.create(
            user=self.teacher,
            user_type='teacher'
        )
        
        # Créer un autre enseignant
        self.other_teacher = User.objects.create_user(
            username='autre_prof',
            email='autre@test.com',
            password='testpass123',
            first_name='Autre',
            last_name='Professeur'
        )
        
        # Créer un profil pour l'autre enseignant
        UserProfile.objects.create(
            user=self.other_teacher,
            user_type='teacher'
        )
        
        # Créer une ressource publique
        self.public_resource = Resource.objects.create(
            owner=self.teacher,
            email=self.teacher.email,
            title='Ressource Publique',
            subject='Math',
            level='L1',
            resource_type='Cours',
            file='public.pdf',
            permission=1,  # Public
            keywords=['math', 'cours']
        )
        
        # Créer une ressource privée
        self.private_resource = Resource.objects.create(
            owner=self.teacher,
            email=self.teacher.email,
            title='Ressource Privée',
            subject='Physique',
            level='L1',
            resource_type='TD',
            file='private.pdf',
            permission=0,  # Privé
            keywords=['physique', 'td']
        )
    
    def test_teacher_home_view_authenticated(self):
        """Test l'accès à la page d'accueil en tant qu'enseignant connecté"""
        self.client.login(username='prof_test', password='testpass123')
        response = self.client.get(reverse('teacher_home'))
        self.assertEqual(response.status_code, 200)
        # Vérifier que le template correct est utilisé
        self.assertTemplateUsed(response, 'teacherhome.html')
        # Vérifier que les clés de contexte attendues sont présentes
        self.assertIn('profile', response.context)
        self.assertIn('form', response.context)
        self.assertIn('files_data', response.context)
        # Vérifier que seules les ressources de l'enseignant connecté sont présentes
        user_resources = list(response.context['files_data'])
        self.assertEqual(len(user_resources), 2)  # public_resource et private_resource
        self.assertTrue(all(res.owner == self.teacher for res in user_resources))
    
    def test_teacher_home_view_unauthenticated(self):
        """Test la redirection si utilisateur non connecté"""
        response = self.client.get(reverse('teacher_home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('teacher_home')}")
    
    def test_upload_resource_view_get(self):
        """Test l'affichage du formulaire d'upload"""
        self.client.login(username='prof_test', password='testpass123')
        response = self.client.get(reverse('upload_form'))
        
        # La vue redirige vers la page d'accueil en GET
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_home'))
    
    def test_upload_resource_view_post_valid(self):
        """Test l'upload d'une nouvelle ressource avec des données valides"""
        self.client.login(username='prof_test', password='testpass123')
        
        # Créer un fichier de test pour l'upload
        test_file = SimpleUploadedFile(
            'new_file.pdf',
            b'file_content',
            content_type='application/pdf'
        )
        
        # Données du formulaire
        data = {
            'title': 'Nouvelle ressource',
            'subject': 'Informatique',
            'level': 'L3',
            'resource_type': 'cours',  # Utiliser la valeur en minuscules pour correspondre aux choix
            'file': test_file,
            'permission': 1,  # Public
            'keywords': 'nouveau, test',  # Espace après la virgule pour tester le nettoyage
        }
        
        # Compter le nombre de ressources avant l'ajout
        initial_count = Resource.objects.count()
        
        # Soumettre le formulaire avec les données et les fichiers
        response = self.client.post(
            reverse('upload_form'),
            data,
            format='multipart'
        )
        
        # Vérifier la redirection après succès
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_home'))
        
        # Vérifier qu'une nouvelle ressource a été créée
        self.assertEqual(Resource.objects.count(), initial_count + 1)
        
        # Vérifier que la ressource a été créée avec les bonnes valeurs
        new_resource = Resource.objects.filter(title='Nouvelle ressource').first()
        self.assertIsNotNone(new_resource)
        self.assertEqual(new_resource.owner, self.teacher)
        self.assertEqual(new_resource.permission, 1)  # Public
        self.assertEqual(new_resource.resource_type, 'cours')
        
        # Vérifier que les mots-clés sont correctement enregistrés
        if hasattr(new_resource, 'keywords'):
            # Vérifier que les mots-clés sont une liste
            self.assertIsInstance(new_resource.keywords, list)
            # Vérifier que les mots-clés ont été correctement nettoyés
            self.assertIn('nouveau', new_resource.keywords)
            self.assertIn('test', new_resource.keywords)
            self.assertEqual(len(new_resource.keywords), 2)
            self.assertCountEqual(new_resource.keywords, ['nouveau', 'test'])
        # Si les mots-clés sont stockés sous forme de chaîne séparée par des virgules
        elif isinstance(new_resource.keywords, str):
            keywords = [k.strip() for k in new_resource.keywords.split(',')]
            self.assertCountEqual(keywords, ['nouveau', 'test'])
    
    def test_edit_resource_view_get(self):
        """Test l'affichage du formulaire d'édition d'une ressource"""
        self.client.login(username='prof_test', password='testpass123')
        response = self.client.get(reverse('edit_resource', args=[self.public_resource.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_resource.html')
        self.assertIn('form', response.context)
        self.assertIn('profile', response.context)
        self.assertEqual(response.context['form'].instance, self.public_resource)
    
    def test_edit_resource_view_post_valid(self):
        """Test la mise à jour d'une ressource avec des données valides"""
        self.client.login(username='prof_test', password='testpass123')
        
        # Données de mise à jour
        data = {
            'title': 'Ressource Modifiée',
            'subject': 'Math Modifié',
            'level': 'L2',
            'resource_type': 'td',  # Utiliser la valeur en minuscules
            'permission': 0,  # Privé
            'keywords': 'modifié,test',
            'email': 'prof@test.com'  # L'email est requis par le formulaire
        }
        
        # Ajouter le fichier s'il est requis par le formulaire
        test_file = SimpleUploadedFile(
            'updated_file.pdf',
            b'updated_content',
            content_type='application/pdf'
        )
        data['file'] = test_file
        
        # Effectuer la requête POST
        response = self.client.post(
            reverse('edit_resource', args=[self.public_resource.id]),
            data,
            follow=True  # Suivre la redirection
        )
        
        # Vérifier la redirection vers la page d'accueil
        self.assertEqual(response.status_code, 200)  # Après la redirection
        
        # Vérifier que la ressource a bien été mise à jour
        updated_resource = Resource.objects.get(id=self.public_resource.id)
        self.assertEqual(updated_resource.title, 'Ressource Modifiée')
        self.assertEqual(updated_resource.subject, 'Math Modifié')
        self.assertEqual(updated_resource.level, 'L2')
        self.assertEqual(updated_resource.resource_type, 'td')
        self.assertEqual(updated_resource.permission, 0)
        
        # Vérifier que les mots-clés sont correctement mis à jour (selon l'implémentation du modèle)
        if hasattr(updated_resource, 'keywords'):
            # Si les mots-clés sont stockés sous forme de liste
            if isinstance(updated_resource.keywords, list):
                self.assertCountEqual(updated_resource.keywords, ['modifié', 'test'])
            # Si les mots-clés sont stockés sous forme de chaîne séparée par des virgules
            elif isinstance(updated_resource.keywords, str):
                keywords = [k.strip() for k in updated_resource.keywords.split(',')]
                self.assertCountEqual(keywords, ['modifié', 'test'])
    
    def test_delete_resource_view(self):
        """Test la suppression d'une ressource"""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        self.client.login(username='prof_test', password='testpass123')
        
        # Créer un fichier de test pour la ressource à supprimer
        test_file = SimpleUploadedFile(
            'todelete.pdf',
            b'content to delete',
            content_type='application/pdf'
        )
        
        # Créer la ressource avec le fichier
        resource_to_delete = Resource.objects.create(
            owner=self.teacher,
            email=self.teacher.email,
            title='À supprimer',
            subject='Informatique',
            level='L1',
            resource_type='autre',  # Utiliser la valeur en minuscules
            file=test_file,
            permission=1,
            keywords=['test']
        )
        
        # Vérifier que le fichier existe physiquement
        import os
        file_path = resource_to_delete.file.path
        self.assertTrue(os.path.exists(file_path))
        
        # Compter le nombre de ressources avant suppression
        initial_count = Resource.objects.count()
        
        # Effectuer la suppression
        response = self.client.post(reverse('delete_file', args=[resource_to_delete.id]), follow=True)
        
        # Vérifier la redirection vers la page d'accueil
        self.assertEqual(response.status_code, 200)  # Après la redirection
        
        # Vérifier que la ressource a bien été supprimée de la base de données
        self.assertEqual(Resource.objects.count(), initial_count - 1)
        self.assertFalse(Resource.objects.filter(id=resource_to_delete.id).exists())
        
        # Vérifier que le fichier physique a été supprimé
        self.assertFalse(os.path.exists(file_path))
    
    def test_download_resource(self):
        """Test le téléchargement d'une ressource"""
        self.client.login(username='prof_test', password='testpass123')
        response = self.client.get(reverse('download_file', args=[self.public_resource.id]))
        
        # La vue renvoie une réponse 200 avec un contenu vide car le fichier n'existe pas réellement
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
    
    def test_search_resources(self):
        """Test la recherche de ressources"""
        self.client.login(username='prof_test', password='testpass123')
        
        # Recherche par titre
        response = self.client.get(reverse('teacher_home'), {'search': 'Publique'})
        self.assertEqual(response.status_code, 200)
        files_data = list(response.context['files_data'])
        self.assertEqual(len(files_data), 1)
        self.assertEqual(files_data[0], self.public_resource)
        
        # Recherche par type de ressource
        response = self.client.get(reverse('teacher_home'), {'resource_type': 'TD'})
        self.assertEqual(response.status_code, 200)
        files_data = list(response.context['files_data'])
        self.assertEqual(len(files_data), 1)
        self.assertEqual(files_data[0], self.private_resource)


class ResourcePermissionTests(TestCase):
    def setUp(self):
        # Créer deux enseignants
        self.teacher1 = User.objects.create_user(
            username='prof1',
            email='prof1@test.com',
            password='testpass123'
        )
        
        # Créer un profil pour le premier enseignant
        UserProfile.objects.create(
            user=self.teacher1,
            user_type='teacher'
        )
        
        self.teacher2 = User.objects.create_user(
            username='prof2',
            email='prof2@test.com',
            password='testpass123'
        )
        
        # Créer un profil pour le deuxième enseignant
        UserProfile.objects.create(
            user=self.teacher2,
            user_type='teacher'
        )
        
        # Créer une ressource pour le premier enseignant
        self.resource = Resource.objects.create(
            owner=self.teacher1,
            email=self.teacher1.email,
            title='Ressource protégée',
            subject='Informatique',
            level='M1',
            resource_type='Cours',
            file='protected.pdf',
            permission=0  # Privé
        )
    
    def test_edit_other_teacher_resource_denied(self):
        """Test qu'un enseignant ne peut pas modifier la ressource d'un autre enseignant"""
        # Se connecter en tant qu'un autre enseignant
        self.client.login(username='prof2', password='testpass123')
        
        response = self.client.get(reverse('edit_resource', args=[self.resource.id]))
        
        # Doit renvoyer une erreur 403 (Forbidden) ou rediriger vers no_access
        self.assertIn(response.status_code, [302, 403])
        if response.status_code == 302:
            self.assertIn('no_access', response.url)
    
    def test_delete_other_teacher_resource_denied(self):
        """Test qu'un enseignant ne peut pas supprimer la ressource d'un autre enseignant"""
        # Se connecter en tant qu'un autre enseignant
        self.client.login(username='prof2', password='testpass123')
        
        response = self.client.post(reverse('delete_file', args=[self.resource.id]))
        
        # Doit renvoyer une erreur 403 (Forbidden) ou rediriger vers no_access
        self.assertIn(response.status_code, [302, 403])
        if response.status_code == 302:
            self.assertIn('no_access', response.url)
        
        # Vérifier que la ressource n'a pas été supprimée
        self.assertTrue(Resource.objects.filter(id=self.resource.id).exists())
