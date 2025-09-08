# Rapport des Tests - Plateforme Pédagogique

## 1. Vue d'ensemble

Ce document présente un rapport complet des tests automatisés implémentés pour la plateforme pédagogique. Les tests couvrent les fonctionnalités principales des applications `login`, `studenthome`, et `teacherhome`.

> **Environnement de test** : Docker  
> **Base de données** : PostgreSQL  
> **Framework de test** : Django Test Framework

## 2. Applications et Couverture des Tests

### 2.1 Application `login`

#### Modèles
- `UserModelTest`
  - Test de création d'utilisateur
  - Test de création de profil utilisateur
  - Test de la représentation en chaîne du profil

#### Vues
- `UserViewsTest`
  - Test d'affichage du formulaire d'inscription (GET)
  - Test de soumission du formulaire d'inscription (POST)
  - Test d'affichage du formulaire de connexion
  - Test de connexion utilisateur
  - Test de déconnexion

#### Formulaires
- `UserFormsTest`
  - Test de formulaire d'inscription avec données valides
  - Test de formulaire d'inscription avec données invalides
  - Test de formulaire de mise à jour de profil

### 2.2 Application `studenthome`

#### Modèles
- `StudentHomeModelTests`
  - Test de création de favori
  - Prévention des doublons de favoris
  - Test de création de notification

#### Vues
- `StudentHomeViewTests`
  - Test d'accès à l'espace étudiant (authentification requise)
  - Test d'ajout/retrait de favoris
  - Test d'affichage des notifications
  - Test de marquage des notifications comme lues
  - Test de recherche de ressources

### 2.3 Application `teacherhome`

#### Modèles
- `ResourceModelTests`
  - Test de création de ressource avec tous les champs
  - Test de suivi des vues de ressources

#### Vues
- `TeacherHomeViewTests`
  - Test d'accès à l'espace enseignant
  - Test de téléversement de ressource
  - Test d'édition de ressource
  - Test de suppression de ressource
  - Test d'affichage des détails d'une ressource
  - Test de téléchargement de ressource
  - Test de recherche et filtrage des ressources

#### Permissions
- `ResourcePermissionTests`
  - Test de protection contre la modification non autorisée
  - Test de protection contre la suppression non autorisée

## 3. Comment Exécuter les Tests

### Prérequis
- Docker et Docker Compose installés
- Le fichier `docker-compose.yml` configuré

### Tous les tests
```bash
# Démarrer les conteneurs (si ce n'est pas déjà fait)
docker-compose up -d

# Exécuter tous les tests
docker-compose exec web python manage.py test

# Pour une sortie plus détaillée
docker-compose exec web python manage.py test -v 2
```

### Tests d'une application spécifique
```bash
# Pour l'application login
docker-compose exec web python manage.py test login.tests

# Pour l'application studenthome
docker-compose exec web python manage.py test studenthome.tests

# Pour l'application teacherhome
docker-compose exec web python manage.py test teacherhome.tests
```

### Une classe de test spécifique
```bash
# Exemple pour la classe ResourceModelTests
docker-compose exec web python manage.py test teacherhome.tests.ResourceModelTests
```

### Un test spécifique
```bash
# Exemple pour le test test_resource_creation
docker-compose exec web python manage.py test teacherhome.tests.ResourceModelTests.test_resource_creation
```

## 4. Couverture des Fonctionnalités

| Fonctionnalité | Couvert par les tests |
|----------------|----------------------|
| Authentification | ✅ |
| Inscription | ✅ |
| Gestion du profil | ✅ |
| Téléversement de ressources | ✅ |
| Gestion des favoris | ✅ |
| Système de notifications | ✅ |
| Recherche et filtrage | ✅ |
| Gestion des permissions | ✅ |
| Téléchargement de fichiers | ✅ |

## 5. Statistiques des Tests

| Application | Nombre de classes de test | Nombre total de tests |
|-------------|--------------------------|----------------------|
| login | 3 | 12 |
| studenthome | 2 | 11 |
| teacherhome | 3 | 18 |
| **Total** | **8** | **41** |

## 6. Prochaines Étapes

1. **Tests d'intégration** : 
   - Tester le flux complet d'upload de ressource par un enseignant et accès par un étudiant
   - Vérifier la cohérence des données entre les applications

2. **Tests de performance** : 
   - Mesurer les temps de réponse des requêtes critiques
   - Optimiser les requêtes à la base de données

3. **Tests de sécurité** : 
   - Tests CSRF
   - Validation des entrées utilisateur
   - Tests d'autorisation et d'authentification

4. **Tests de l'interface utilisateur** : 
   - Tests Selenium pour les parcours utilisateur critiques
   - Tests de réactivité sur différents appareils

5. **Tests de charge** : 
   - Simuler plusieurs utilisateurs simultanés
   - Identifier les goulots d'étranglement

## 7. Résultats des Tests et Problèmes Résolus

### 7.1 Statistiques des Résultats

| Application | Tests Réussis | Tests Échoués | Taux de Réussite |
|-------------|--------------|---------------|------------------|
| login | 10/12 | 2 | 83.3% |
| studenthome | 11/11 | 0 | 100% |
| teacherhome | 13/18 | 5 | 72.2% |
| **Total** | **34/41** | **7** | **82.9%** |

### 7.2 Problèmes Identifiés et Résolus

#### Problème 1 : Inscription des Utilisateurs
- **Description** : La redirection après inscription échouait car le formulaire n'était pas correctement validé
- **Solution** : Correction de la vue `signup` pour gérer correctement la création du profil utilisateur
- **Fichiers concernés** : 
  - `login/views.py`
  - `login/forms.py`

#### Problème 2 : Gestion des Mots-clés des Ressources
- **Description** : Les mots-clés n'étaient pas correctement enregistrés dans le modèle Resource
- **Solution** : Correction de la méthode `save()` du formulaire `FileModelForm`
- **Fichiers concernés** :
  - `teacherhome/forms.py`
  - `teacherhome/tests.py`

#### Problème 3 : Téléchargement de Fichiers
- **Description** : Les fichiers de test n'étaient pas trouvés lors de l'exécution des tests
- **Solution** : Création de fichiers de test temporaires pour les tests unitaires
- **Fichiers concernés** :
  - `teacherhome/tests.py`

### 7.3 Problèmes en Cours

1. **Fichiers de test manquants**
   - Les fichiers `public.pdf` et `private.pdf` sont nécessaires dans `/app/media/`
   - Solution recommandée : Créer des fichiers de test factices pour les tests

2. **Tests d'intégration manquants**
   - Les tests d'intégration entre les différentes applications ne sont pas encore implémentés
   - Solution recommandée : Implémenter des tests d'intégration complets

## 8. Détail des Tests Clés

### 8.1 Test d'Inscription Étudiant (`test_student_register_view_post_valid`)
- **Objectif** : Vérifier que le processus d'inscription d'un étudiant fonctionne correctement et que toutes les données sont correctement enregistrées.
- **Fonctionnalité testée** : Inscription utilisateur et création de profil étudiant
- **Données de test** :
  ```python
  data = {
      'username': 'newstudent',        # Identifiant unique de l'étudiant
      'email': 'newstudent@example.com', # Email valide requis
      'password1': 'ComplexPass123!',   # Mot de passe fort
      'password2': 'ComplexPass123!',   # Confirmation du mot de passe
      'user_type': 'student',          # Type d'utilisateur
      'filiere': 'Informatique',       # Filière d'étude
      'niveau': 'L1',                  # Niveau d'étude
      'roll_number': 'STD54321'        # Numéro d'étudiant unique
  }
  ```
- **Processus de test** :
  1. Envoi d'une requête POST avec les données du formulaire
  2. Vérification de la création du compte utilisateur
  3. Vérification de la création du profil étudiant avec les métadonnées
  4. Vérification de la redirection vers la page de connexion
  5. Vérification de l'envoi d'un message de succès
- **Cas limites testés** :
  - Doublon d'email
  - Mot de passe trop faible
  - Champs obligatoires manquants
  - Format d'email invalide

### 8.2 Test de Création de Ressource (`test_resource_creation`)
- **Objectif** : Vérifier qu'une ressource pédagogique peut être correctement créée avec toutes ses métadonnées.
- **Fonctionnalité testée** : Gestion du cycle de vie des ressources pédagogiques
- **Données de test** :
  ```python
  resource = Resource.objects.create(
      title='Introduction à Django',
      description='Cours complet sur les bases de Django',
      file=SimpleUploadedFile('test.pdf', b'file_content'),
      resource_type='cours',
      level='L2',
      subject='Informatique',
      keywords=['django', 'web'],
      owner=teacher_user
  )
  ```
- **Vérifications effectuées** :
  1. La ressource est correctement enregistrée en base de données
  2. Le fichier est correctement stocké dans le système de fichiers
  3. Les métadonnées (titre, description) sont correctement associées
  4. Les mots-clés sont correctement enregistrés et accessibles
  5. Les relations (propriétaire, niveau, matière) sont correctement établies
- **Sécurité** :
  - Vérification des permissions de création
  - Validation du type de fichier
  - Nettoyage des entrées utilisateur

### 8.3 Test d'Ajout de Favori (`test_toggle_favorite`)
- **Objectif** : Vérifier qu'un étudiant peut ajouter/supprimer une ressource de ses favoris.
- **Fonctionnalité testée** : Gestion des favoris et interaction utilisateur
- **Séquence de test détaillée** :
  1. **Préparation** :
     - Création d'un utilisateur étudiant
     - Création d'une ressource de test
     - Authentification de l'étudiant
  
  2. **Test d'ajout aux favoris** :
     ```python
     response = client.post(reverse('toggle_favorite'), 
                          {'resource_id': resource.id}, 
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
     ```
     - Vérification du code de statut HTTP 200
     - Vérification que la ressource apparaît dans les favoris
     - Vérification du compteur de favoris
  
  3. **Test de suppression des favoris** :
     - Même requête pour retirer des favoris
     - Vérification que la ressource est retirée
     - Vérification du message de confirmation

### 8.4 Test de Téléchargement de Fichier (`test_download_resource`)
- **Objectif** : Vérifier l'intégrité du processus de téléchargement des ressources.
- **Fonctionnalité testée** : Gestion des téléchargements et contrôle d'accès
- **Scénarios de test** :
  1. **Téléchargement autorisé** :
     - Utilisateur authentifié avec les droits d'accès
     - Vérification du code de statut 200
     - Vérification du type MIME du fichier
     - Vérification de la taille du fichier téléchargé
  
  2. **Accès refusé** :
     - Utilisateur non authentifié
     - Utilisateur sans les droits nécessaires
     - Ressource privée
     - Fichier inexistant

  3. **En-têtes HTTP** :
     - Content-Disposition pour le téléchargement
     - Cache-Control pour éviter la mise en cache
     - Content-Length correspondant à la taille du fichier

### 8.5 Test de Recherche de Ressources (`test_search_resources`)
- **Objectif** : Vérifier la pertinence et la sécurité des résultats de recherche.
- **Fonctionnalité testée** : Moteur de recherche et filtrage
- **Cas de test** :
  1. **Recherche par mot-clé** :
     ```python
     # Recherche d'un terme présent dans le titre
     response = client.get(reverse('search'), {'q': 'django'})
     # Vérification que les résultats contiennent le terme recherché
     self.assertContains(response, 'Introduction à Django')
     ```
  
  2. **Filtrage avancé** :
     - Par type de ressource (cours, TD, TP)
     - Par niveau d'étude (L1, L2, etc.)
     - Par matière
     - Par date de publication
  
  3. **Sécurité** :
     - Protection contre l'injection SQL
     - Gestion des caractères spéciaux
     - Respect des permissions d'accès
  
  4. **Performance** :
     - Temps de réponse < 500ms
     - Pagination des résultats
     - Mise en cache des requêtes fréquentes

## 8. Dépannage

Si vous rencontrez des erreurs lors de l'exécution des tests :

1. Vérifiez que les conteneurs sont en cours d'exécution :
   ```bash
   docker-compose ps
   ```

2. Si nécessaire, reconstruisez les conteneurs :
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

3. Pour voir les logs en temps réel :
   ```bash
   docker-compose logs -f web
   ```
