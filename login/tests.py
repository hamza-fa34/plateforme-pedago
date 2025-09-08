from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='student',
            niveau='L1',
            filiere='Informatique',
            roll_number='STD12345'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.user_type, 'student')
        self.assertEqual(self.user_profile.niveau, 'L1')
        self.assertEqual(self.user_profile.filiere, 'Informatique')
        self.assertEqual(self.user_profile.roll_number, 'STD12345')
    
    def test_user_profile_str_representation(self):
        self.assertEqual(str(self.user_profile), 'testuser')


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Créer un utilisateur étudiant
        self.student_user = User.objects.create_user(
            username='teststudent',
            email='student@example.com',
            password='testpass123',
            first_name='Étudiant',
            last_name='Test'
        )
        self.student_profile = UserProfile.objects.create(
            user=self.student_user,
            user_type='student',
            niveau='L1',
            filiere='Informatique',
            roll_number='STD12345'
        )
        
        # Créer un utilisateur enseignant
        self.teacher_user = User.objects.create_user(
            username='testteacher',
            email='teacher@example.com',
            password='testpass123',
            first_name='Professeur',
            last_name='Test'
        )
        self.teacher_profile = UserProfile.objects.create(
            user=self.teacher_user,
            user_type='teacher',
            niveau='',
            filiere='',
            roll_number=''
        )
    
    def test_register_view_get(self):
        """Test l'affichage de la page d'inscription"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIn('form', response.context)
    
    def test_student_register_view_post_valid(self):
        """Test l'inscription d'un nouvel étudiant"""
        data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'first_name': 'Nouvel',
            'last_name': 'Étudiant',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'student',
            'filiere': 'Informatique',
            'niveau': 'L1',
            'roll_number': 'STD54321'
        }
        response = self.client.post(reverse('signup'), data)
        
        # Vérifier la redirection après inscription réussie
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(username='newstudent').exists())
        
        # Vérifier que le profil étudiant a été créé avec les bonnes données
        new_user = User.objects.get(username='newstudent')
        self.assertTrue(hasattr(new_user, 'userprofile'))
        self.assertEqual(new_user.userprofile.user_type, 'student')
        self.assertEqual(new_user.userprofile.filiere, 'Informatique')
        self.assertEqual(new_user.userprofile.niveau, 'L1')
        self.assertEqual(new_user.userprofile.roll_number, 'STD54321')
    
    def test_teacher_register_view_post_valid(self):
        """Test l'inscription d'un nouvel enseignant"""
        data = {
            'username': 'newteacher',
            'email': 'newteacher@example.com',
            'first_name': 'Nouveau',
            'last_name': 'Enseignant',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'teacher',
            'filiere': '',
            'niveau': '',
            'roll_number': ''
        }
        response = self.client.post(reverse('signup'), data)
        
        # Vérifier la redirection après inscription réussie
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(username='newteacher').exists())
        
        # Vérifier que le profil enseignant a été créé
        new_user = User.objects.get(username='newteacher')
        self.assertTrue(hasattr(new_user, 'userprofile'))
        self.assertEqual(new_user.userprofile.user_type, 'teacher')
        self.assertEqual(new_user.userprofile.filiere, '')
        self.assertEqual(new_user.userprofile.niveau, '')
        self.assertEqual(new_user.userprofile.roll_number, '')
    
    def test_student_login_redirect(self):
        """Test la redirection après connexion d'un étudiant"""
        response = self.client.post(
            reverse('login'),
            {'username': 'teststudent', 'password': 'testpass123'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que l'utilisateur est redirigé vers la page d'accueil des étudiants
        self.assertIn('studenthome', response.request['PATH_INFO'])
    
    def test_teacher_login_redirect(self):
        """Test la redirection après connexion d'un enseignant"""
        response = self.client.post(
            reverse('login'),
            {'username': 'testteacher', 'password': 'testpass123'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que l'utilisateur est redirigé vers la page d'accueil des enseignants
        self.assertIn('teacherhome', response.request['PATH_INFO'])
    
    def test_logout_view(self):
        """Test la déconnexion d'un utilisateur"""
        # Se connecter d'abord
        self.client.login(username='teststudent', password='testpass123')
        
        # Tester la déconnexion
        response = self.client.get(reverse('logout'), follow=True)
        
        # Vérifier que l'utilisateur est redirigé vers la page de connexion
        self.assertEqual(response.status_code, 200)
        self.assertIn('login', response.request['PATH_INFO'])
        
        # Vérifier que l'utilisateur est bien déconnecté
        self.assertFalse('_auth_user_id' in self.client.session)


class UserFormsTest(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests de mise à jour
        self.user = User.objects.create_user(
            username='testformuser',
            email='testform@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            user_type='student',
            niveau='L1',
            filiere='Informatique',
            roll_number='STD00000'
        )
    
    def test_student_register_form_valid_data(self):
        """Test le formulaire d'inscription étudiant avec des données valides"""
        form_data = {
            'username': 'newstudentform',
            'email': 'newstudent@example.com',
            'first_name': 'Étudiant',
            'last_name': 'Form',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'student',
            'filiere': 'mathematiques',  # Utiliser la clé exacte du choix
            'niveau': 'L2',
            'roll_number': 'STD99999'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_teacher_register_form_valid_data(self):
        """Test le formulaire d'inscription enseignant avec des données valides"""
        form_data = {
            'username': 'newteacherform',
            'email': 'newteacher@example.com',
            'first_name': 'Professeur',
            'last_name': 'Form',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'user_type': 'teacher',
            'filiere': '',
            'niveau': '',
            'roll_number': ''
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_register_form_missing_required_fields(self):
        """Test le formulaire d'inscription avec des champs obligatoires manquants"""
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
            'user_type': ''
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('user_type', form.errors)
    
    def test_register_form_password_mismatch(self):
        """Test le formulaire d'inscription avec des mots de passe différents"""
        form_data = {
            'username': 'passwordtest',
            'email': 'password@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!',
            'user_type': 'student',
            'filiere': 'Informatique',
            'niveau': 'L1',
            'roll_number': 'STD12345'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_user_update_form(self):
        """Test le formulaire de mise à jour du profil utilisateur"""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Sauvegarder le formulaire et vérifier les mises à jour
        user = form.save()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.email, 'updated@example.com')
    
    def test_profile_update_form_teacher(self):
        """Test le formulaire de mise à jour du profil enseignant"""
        # Changer le profil en enseignant
        self.profile.user_type = 'teacher'
        self.profile.save()
        
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Teacher',
            'email': 'updated@example.com',
            'user_type': 'teacher',
            'filiere': '',  # Champs facultatifs pour un enseignant
            'niveau': '',
            'roll_number': ''
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Sauvegarder le formulaire et vérifier les mises à jour
        profile = form.save()
        user = profile.user
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Teacher')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(profile.user_type, 'teacher')
    
    def test_profile_update_form_student(self):
        """Test le formulaire de mise à jour du profil étudiant"""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Student',
            'email': 'updated@example.com',
            'user_type': 'student',
            'filiere': 'physique',  # Utiliser la clé exacte du choix
            'niveau': 'L3',
            'roll_number': 'STD54321'
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Sauvegarder le formulaire et vérifier les mises à jour
        profile = form.save()
        user = profile.user
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Student')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(profile.user_type, 'student')
        self.assertEqual(profile.niveau, 'L3')
        self.assertEqual(profile.filiere, 'physique')
        self.assertEqual(profile.roll_number, 'STD54321')
    
    def test_profile_update_form_teacher(self):
        """Test le formulaire de mise à jour du profil enseignant"""
        # Créer un profil enseignant
        teacher = User.objects.create_user(
            username='teacherform',
            email='teacherform@example.com',
            password='testpass123',
            first_name='Teacher',
            last_name='Form'
        )
        teacher_profile = UserProfile.objects.create(
            user=teacher,
            user_type='teacher'
        )
        
        # Données de mise à jour du formulaire
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Teacher',
            'email': 'updated.teacher@example.com',
            'user_type': 'teacher',
            'niveau': '',
            'filiere': '',
            'roll_number': ''
        }
        form = ProfileUpdateForm(data=form_data, instance=teacher_profile, user=teacher)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Sauvegarder le formulaire et vérifier les mises à jour
        profile = form.save()
        user = profile.user
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Teacher')
        self.assertEqual(user.email, 'updated.teacher@example.com')
        self.assertEqual(profile.user_type, 'teacher')
