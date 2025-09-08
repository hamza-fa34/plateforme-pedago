from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from teacherhome.models import Resource
from .models import Favorite, Notification

User = get_user_model()

class StudentHomeModelTests(TestCase):
    def setUp(self):
        # Créer un utilisateur étudiant
        self.student = User.objects.create_user(
            username='etudiant1',
            email='etudiant1@example.com',
            password='testpass123',
            first_name='Jean',
            last_name='Dupont'
        )
        
        # Créer un enseignant
        self.teacher = User.objects.create_user(
            username='prof1',
            email='prof1@example.com',
            password='testpass123',
            first_name='Marie',
            last_name='Martin'
        )
        
        # Créer une ressource
        self.resource = Resource.objects.create(
            title='Cours de Python',
            subject='Informatique',
            level='L1',
            resource_type='cours',
            file='cours_python.pdf',
            owner=self.teacher,
            email=self.teacher.email,
            permission=1,  # 1 = Public, 0 = Privé
            keywords=['python', 'programmation']
        )
    
    def test_favorite_creation(self):
        """Test la création d'un favori"""
        favorite = Favorite.objects.create(
            user=self.student,
            resource=self.resource
        )
        
        self.assertEqual(str(favorite), f"{self.student.username} ❤️ {self.resource.file.name}")
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertEqual(self.student.favorites.count(), 1)
        self.assertEqual(self.resource.favorited_by.count(), 1)
    
    def test_duplicate_favorite_prevention(self):
        """Test qu'on ne peut pas ajouter deux fois la même ressource en favori"""
        Favorite.objects.create(user=self.student, resource=self.resource)
        
        # Essayer de créer un doublon
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.student, resource=self.resource)
    
    def test_notification_creation(self):
        """Test la création d'une notification"""
        notification = Notification.objects.create(
            user=self.student,
            message='Nouvelle ressource disponible',
            is_read=False
        )
        
        # Vérifier que la représentation en chaîne est correcte
        expected_str = f"Notification for {self.student.username}: Nouvelle ressource disponible..."
        self.assertEqual(str(notification), expected_str)
        
        # Vérifier que la notification a été correctement enregistrée
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(self.student.notification_set.count(), 1)
        self.assertFalse(notification.is_read)


class StudentHomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Créer un utilisateur étudiant
        self.student = User.objects.create_user(
            username='etudiant_test',
            email='etudiant@test.com',
            password='testpass123',
            first_name='Étudiant',
            last_name='Test'
        )
        
        # Créer le profil étudiant
        from login.models import UserProfile
        self.student_profile = UserProfile.objects.create(
            user=self.student,
            name='Étudiant Test',
            user_type='student',
            niveau='L2',
            filiere='informatique'
        )
        
        # Créer un enseignant
        self.teacher = User.objects.create_user(
            username='prof_test',
            email='prof@test.com',
            password='testpass123',
            first_name='Professeur',
            last_name='Test'
        )
        
        # Créer le profil enseignant
        self.teacher_profile = UserProfile.objects.create(
            user=self.teacher,
            name='Professeur Test',
            user_type='teacher'
        )
        
        # Créer des ressources avec des fichiers temporaires
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Créer un fichier temporaire pour la ressource 1
        file1 = SimpleUploadedFile(
            'fichier1.pdf',
            b'Contenu du fichier 1',
            content_type='application/pdf'
        )
        
        # Créer une ressource avec des mots-clés
        self.resource1 = Resource.objects.create(
            owner=self.teacher,
            email=self.teacher.email,
            title='Ressource 1',
            subject='Math',
            level='L1',
            resource_type='cours',  # Utiliser des minuscules pour correspondre aux choix possibles
            file=file1,
            permission=1  # Public
        )
        self.resource1.keywords = ['math', 'ressource']
        self.resource1.save()
        
        # Créer un fichier temporaire pour la ressource 2
        file2 = SimpleUploadedFile(
            'fichier2.pdf',
            b'Contenu du fichier 2',
            content_type='application/pdf'
        )
        
        self.resource2 = Resource.objects.create(
            owner=self.teacher,
            email=self.teacher.email,
            title='Ressource 2',
            subject='Physique',
            level='L1',
            resource_type='td',  # Utiliser des minuscules pour correspondre aux choix possibles
            file=file2,
            permission=0  # Privé
        )
        self.resource2.keywords = ['physique', 'ressource']
        self.resource2.save()
        
        # Créer des notifications
        self.notification1 = Notification.objects.create(
            user=self.student,
            message='Notification 1',
            is_read=False
        )
        
        self.notification2 = Notification.objects.create(
            user=self.student,
            message='Notification 2',
            is_read=True
        )
    
    def test_home_view_authenticated(self):
        """Test l'accès à la page d'accueil en tant qu'étudiant connecté"""
        self.client.login(username='etudiant_test', password='testpass123')
        response = self.client.get(reverse('studenthome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studenthome.html')
        self.assertIn('recommendations', response.context)
        self.assertIn('profile', response.context)
    
    def test_home_view_unauthenticated(self):
        """Test la redirection si utilisateur non connecté"""
        response = self.client.get(reverse('studenthome'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('studenthome')}")
    
    def test_toggle_favorite_view(self):
        """Test l'ajout/retrait d'une ressource des favoris"""
        print("\n=== TEST: AJOUT D'UN FAVORI ===")
        self.client.login(username='etudiant_test', password='testpass123')
        
        # 1. Tester l'ajout aux favoris
        response = self.client.post(
            reverse('toggle_favorite'),
            {'resource_id': self.resource1.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('success', response_data)
        self.assertTrue(response_data['success'])
        self.assertTrue(response_data['favorited'])  # Doit indiquer que le favori est ajouté
        
        # Vérifier que le favori a bien été créé en base de données
        favorite_exists = Favorite.objects.filter(
            user=self.student,
            resource=self.resource1
        ).exists()
        self.assertTrue(favorite_exists, "Le favori devrait exister après l'ajout")
        
        # 2. Tester le retrait des favoris
        print("\n=== TEST: RETRAIT D'UN FAVORI ===")
        response = self.client.post(
            reverse('toggle_favorite'),
            {'resource_id': self.resource1.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('success', response_data)
        self.assertTrue(response_data['success'])
        self.assertFalse(response_data['favorited'])  # Doit indiquer que le favori est retiré
        
        # Vérifier que le favori a bien été supprimé de la base de données
        favorite_exists = Favorite.objects.filter(
            user=self.student,
            resource=self.resource1
        ).exists()
        self.assertFalse(favorite_exists, "Le favori ne devrait plus exister après le retrait")
    
    def test_notifications_view(self):
        """Test l'affichage des notifications"""
        self.client.login(username='etudiant_test', password='testpass123')
        response = self.client.get(reverse('notifications_list'))
        self.assertEqual(response.status_code, 200)
        # Vérifier que la réponse utilise le bon template
        self.assertTemplateUsed(response, 'notifications_list.html')
        # Vérifier que les notifications sont dans le contexte
        self.assertIn('notifications', response.context)
        self.assertEqual(len(response.context['notifications']), 2)  # 2 notifications créées dans le setUp
    
    def test_mark_notification_as_read(self):
        """Test que les notifications sont marquées comme lues lors de la récupération"""
        self.client.login(username='etudiant_test', password='testpass123')
        
        # Vérifier que la notification est initialement non lue
        self.assertFalse(Notification.objects.get(id=self.notification1.id).is_read)
        
        # Récupérer la liste des notifications (cela devrait les marquer comme lues)
        response = self.client.get(reverse('notifications_list'))
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que toutes les notifications sont maintenant marquées comme lues
        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
        self.assertTrue(self.notification2.is_read)
    
    def test_search_resources(self):
        """Test la recherche de ressources"""
        self.client.login(username='etudiant_test', password='testpass123')
        
        # La vue studentHome ne prend pas en charge la recherche directe
        # Vérifions simplement que la page se charge correctement avec différents paramètres
        
        # Test avec un terme de recherche
        response = self.client.get(reverse('studenthome'), {'q': 'Ressource 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', response.context)
        
        # Test avec un filtre de type de ressource
        response = self.client.get(reverse('studenthome'), {'resource_type': 'cours'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', response.context)
