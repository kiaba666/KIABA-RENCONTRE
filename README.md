# KIABA - Petites annonces Côte d'Ivoire

Application web de petites annonces pour adultes, orientée Côte d'Ivoire, développée avec Django/Python.

## 🚨 Contraintes importantes

- **18+ uniquement** : Contenu réservé aux majeurs
- **Aucun prix** : Aucun tarif stocké ni affiché
- **Prestataires seulement** : Seuls les prestataires s'inscrivent et publient
- **Visiteurs libres** : Consultation sans compte requis
- **Maximum 5 photos** par annonce
- **Contact uniquement** : SMS/WhatsApp/Appel (deep links)

## 🛠 Stack technique

- **Backend** : Django 5.x, Python 3.12, PostgreSQL 15+
- **Frontend** : Django Templates + Tailwind CSS, HTMX
- **Auth** : django-allauth (inscription limitée aux prestataires)
- **Cache** : Redis (cache + rate limit)
- **Tasks** : Celery + Celery Beat
- **Storage** : django-storages (S3 compatible) ou FileSystemStorage
- **Images** : Pillow + django-imagekit (redimensionnement, compression)
- **SEO** : django-sitemaps, robots.txt, meta dynamiques
- **Tests** : pytest + pytest-django, coverage
- **DevOps** : Docker + docker-compose, GitHub Actions

## 🚀 Installation rapide

### Prérequis

- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- Docker (optionnel)

### 1. Cloner et configurer

```bash
cd ~/Desktop/KIABA
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Configuration environnement

```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

### 3. Base de données

```bash
# Créer la base PostgreSQL
createdb kiaba

# Migrations
python manage.py migrate

# Superutilisateur
python manage.py createsuperuser
```

### 4. Lancer l'application

```bash
# Terminal 1 - Serveur web
python manage.py runserver

# Terminal 2 - Celery worker
celery -A kiaba worker -l info

# Terminal 3 - Celery beat (tâches périodiques)
celery -A kiaba beat -l info
```

## 🐳 Docker (recommandé)

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

## 📧 Configuration e-mail

Le projet est configuré pour utiliser `support@ci-kiaba.com` :

```bash
# Test d'envoi
python manage.py email_test votre@email.com
```

### Configuration DNS recommandée

```
# SPF
Ajoutez un enregistrement SPF pour votre domaine (exemple LWS) et DKIM/DMARC via votre hébergeur.

# DKIM
# Demander les enregistrements DKIM à votre hébergeur

# DMARC
_dmarc.ci-kiaba.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@ci-kiaba.com"
```

## 🧪 Tests

```bash
# Tests unitaires
python manage.py test

# Avec coverage
coverage run --source='.' manage.py test
coverage report

# Linting
flake8
black --check .
isort --check-only .
```

## 📁 Structure du projet

```
KIABA/
├── accounts/          # Utilisateurs et profils
├── ads/              # Annonces et médias
├── core/             # Vues principales et middleware
├── moderation/       # Modération des annonces
├── seo/              # Sitemaps et robots.txt
├── templates/        # Templates Django
├── static/           # Fichiers statiques
├── media/            # Médias uploadés
├── .env.example      # Variables d'environnement
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🔧 Commandes utiles

```bash
# Développement
make dev              # Installer les dépendances
make migrate          # Appliquer les migrations
make run              # Lancer le serveur
make superuser        # Créer un superutilisateur

# Qualité
make lint             # Vérifier le code
make format           # Formater le code
make test             # Lancer les tests
make coverage         # Rapport de couverture

# Production
make static           # Collecter les fichiers statiques
```

## 🌍 SEO et conformité

### Pages générées automatiquement

- `/sitemap.xml` - Sitemap des annonces et villes
- `/robots.txt` - Instructions pour les moteurs de recherche
- Pages ville × catégorie (ex: `/ads?city=abidjan&category=escorte_girl`)

### Age-gate

- Middleware redirige vers `/age-gate/` si cookie manquant
- Cookie `age_gate_accepted` valide l'accès

### Modération

- Workflow : draft → pending → approved/rejected → archived
- Logs d'audit pour toutes les actions sensibles
- Filtrage automatique des contenus inappropriés

## 📊 Catégories et sous-catégories

### Escorte girls

- vaginal, sodomie, massage sexuel, massage africain, fellation

### Escorte boy

- Services masculins

### Transgenre

- Services transgenres

## 🔒 Sécurité

- Rate limiting (Redis)
- CSRF protection
- XSS protection (bleach)
- Content Security Policy
- Validation stricte des uploads (max 5 photos)
- Sanitisation HTML des descriptions

## 🚀 Déploiement

### Variables d'environnement critiques

```bash
DEBUG=false
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=kiaba.ci,www.kiaba.ci
POSTGRES_DB=kiaba
POSTGRES_USER=kiaba
POSTGRES_PASSWORD=secure-password
REDIS_URL=redis://localhost:6379/1
```

### Checklist déploiement

- [ ] Base PostgreSQL créée
- [ ] Redis démarré
- [ ] Variables d'environnement configurées
- [ ] Migrations appliquées
- [ ] Fichiers statiques collectés
- [ ] Celery worker/beat démarrés
- [ ] Certificat SSL configuré
- [ ] DNS configuré (SPF, DKIM, DMARC)

## 📞 Support

Pour toute question technique :

- Email : support@ci-kiaba.com
- Documentation : Voir les commentaires dans le code

## ⚖️ Légal

- **18+ uniquement** - Vérification d'âge obligatoire
- **Aucun contenu explicite** - Images et textes modérés
- **Respect de la vie privée** - Données personnelles protégées
- **Conformité locale** - Respect des lois ivoiriennes

---

**KIABA** - Petites annonces Côte d'Ivoire © 2024
