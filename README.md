# Plateforme Pédagogique

> Ce projet est un fork et une adaptation de [Academia Campus Repository](https://github.com/VishalTheHuman/Academia-Campus-Repository) (MIT License).

## 🎯 Périmètre MVP (Minimum Viable Product)

La plateforme, dans sa version MVP, propose uniquement les fonctionnalités suivantes :

- **Comptes et rôles** :
  - Inscription, connexion, déconnexion
  - Gestion des rôles (étudiant, enseignant, admin)
  - Redirections et accès selon le rôle
- **Dépôt de ressources** :
  - Dépôt de fichiers (PDF, vidéo, URL)
  - Extraction automatique de mots-clés
- **Recherche** :
  - Recherche plein-texte sur les ressources
  - Filtres et suggestions (« Trending », « Similaires »)
- **Favoris** :
  - Ajout/suppression de ressources en favoris (⭐)
  - Liste personnelle de favoris
- **Dashboard admin basique** :
  - Statistiques de dépôts, vues, utilisateurs

---

## 🚀 Installation & Lancement

### Prérequis
- Docker et Docker Compose installés

### 1. Cloner le dépôt
```sh
git clone https://github.com/hamza-fa34/plateforme-pedago.git
cd plateforme-pedago
```

### 2. Configurer l'environnement
```sh
cp env.example.txt .env
# Adapter les variables si besoin
```

### 3. Lancer les conteneurs
```sh
docker-compose up --build
```

### 4. Peupler la base avec des comptes de test et ressources
```sh
docker-compose exec web python populate_resources.py
```
- Crée 10 enseignants (`teacher1` à `teacher10`), 50 étudiants (`student1` à `student50`), mot de passe `Azerty123@`.
- Génère 50 ressources réparties entre plusieurs professeurs.

### 5. Accéder à l'application
- http://localhost:8000
- Admin Django : http://localhost:8000/admin

### 6. Commandes utiles
- Arrêter les conteneurs : `docker-compose down`
- Voir les logs : `docker-compose logs -f`
- Redémarrer le service web : `docker-compose restart web`

---

## 🔔 Fonctionnalités avancées
- Système de notifications moderne (page dédiée, badge, design responsive)
- Recommandations personnalisées logiques et évolutives selon l'activité de l'étudiant
- Gestion multi-professeurs pour les ressources
- Comptes de test générés automatiquement pour faciliter les démos et tests

---

## 🗺️ Roadmap (prévisionnelle)

### **Sprint 1 : Stabilisation & Tests du MVP**
- Correction de bugs, stabilisation du code
- Sécurisation des accès et des données
- Tests manuels et automatisés des parcours MVP

### **Sprint 2 : Améliorations UX/UI**
- Accessibilité (a11y)
- Responsive design (mobile/tablette)
- Uniformisation des styles et composants
- Petites améliorations ergonomiques

### **Sprint 3 : Fonctionnalités hors périmètre**
- Réintégration progressive des modules avancés (cours, devoirs, notifications, etc.)
- Déploiement d'API, PWA, analytics, IA, etc.
- Améliorations majeures selon retours utilisateurs

---

## 📄 Licence

MIT. Voir [LICENSE](LICENSE).
