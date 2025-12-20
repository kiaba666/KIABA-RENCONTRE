# Guide : Import d'Annonces depuis ci.jedolo.com

## 📋 Description

Ce script permet d'importer des annonces depuis le site `ci.jedolo.com` et de créer automatiquement :
- **546 utilisateurs** (ou un nombre personnalisé)
- **Au moins 2 annonces par utilisateur** (configurable)
- **Images téléchargées et stockées** dans le dossier `media/ads/`

## 🚀 Installation des Dépendances

Avant d'utiliser le script, installez les dépendances nécessaires :

```bash
pip install beautifulsoup4 requests
```

Ou si vous utilisez `requirements.txt` :

```bash
pip install -r requirements.txt
```

## 📝 Utilisation

### Commande de Base

```bash
python manage.py import_from_jedolo
```

Cette commande créera par défaut :
- 546 utilisateurs
- 2-5 annonces par utilisateur (aléatoire)

### Options Disponibles

```bash
# Créer 546 utilisateurs avec 2-5 annonces chacun (défaut)
python manage.py import_from_jedolo

# Créer 100 utilisateurs avec 2 annonces chacun
python manage.py import_from_jedolo --users 100 --ads-per-user 2

# Créer 546 utilisateurs avec 3-6 annonces chacun
python manage.py import_from_jedolo --users 546 --ads-per-user 3 --max-ads 6
```

### Paramètres

- `--users` : Nombre d'utilisateurs à créer (défaut: 546)
- `--ads-per-user` : Nombre minimum d'annonces par utilisateur (défaut: 2)
- `--max-ads` : Nombre maximum d'annonces par utilisateur (défaut: 5)

## 🔍 Fonctionnement

### 1. Scraping des Annonces

Le script :
- Scrape les annonces depuis `https://ci.jedolo.com/`
- Extrait les titres, descriptions, catégories et images
- Télécharge les images et les stocke dans `media/ads/`

### 2. Création des Utilisateurs

Pour chaque utilisateur :
- Nom d'utilisateur unique généré (ex: `mariekouassi123`)
- Email automatique (ex: `mariekouassi123@example.com`)
- Mot de passe par défaut : `password123`
- Profil créé avec nom ivoirien aléatoire
- Ville assignée aléatoirement

### 3. Création des Annonces

Pour chaque annonce :
- Titre et description depuis le scraping (ou générés)
- Catégorie déterminée automatiquement
- Sous-catégories assignées
- Images téléchargées et stockées
- Statut : `APPROVED` (approuvée)
- Expiration : 14-30 jours

## 📁 Structure des Fichiers

```
media/
  ads/
    ad_1_1.jpg
    ad_1_2.jpg
    ad_2_1.jpg
    ...
```

Les images sont stockées avec le format : `ad_{ad_id}_{image_number}.{ext}`

## ⚠️ Notes Importantes

### Images

- Les images sont téléchargées depuis `ci.jedolo.com`
- Taille maximale : 5MB par image
- Maximum 5 images par annonce
- Si le téléchargement échoue, une image fictive est créée

### Utilisateurs

- Tous les utilisateurs ont le rôle `PROVIDER`
- Mot de passe par défaut : `password123`
- Les emails sont fictifs (`@example.com`)
- Les profils sont créés automatiquement

### Annonces

- Toutes les annonces sont approuvées (`APPROVED`)
- Les descriptions sont sanitizées avec `bleach`
- Les catégories sont déterminées automatiquement
- Les villes sont assignées aléatoirement

## 🔧 Dépannage

### Erreur : "BeautifulSoup4 n'est pas installé"

```bash
pip install beautifulsoup4
```

### Erreur : "Aucune annonce scrapée"

Le script générera automatiquement des annonces fictives si le scraping échoue.

### Erreur : "Image trop volumineuse"

Les images de plus de 5MB sont ignorées. Le script créera une image fictive à la place.

### Erreur : "Utilisateur existe déjà"

Le script génère automatiquement un nom d'utilisateur unique si un conflit survient.

## 📊 Résultats Attendus

Après l'exécution, vous devriez avoir :

- ✅ 546 utilisateurs créés
- ✅ 1092-2730 annonces créées (2-5 par utilisateur)
- ✅ Images stockées dans `media/ads/`
- ✅ Toutes les annonces approuvées et visibles sur le site

## 🎯 Exemple d'Exécution

```bash
$ python manage.py import_from_jedolo --users 546 --ads-per-user 2

Début de l'import: 546 utilisateurs, 2-5 annonces par utilisateur
Scraping des annonces depuis ci.jedolo.com...
  → 45 annonces scrapées
  → 50 utilisateurs créés...
  → 100 annonces créées...
  → 100 utilisateurs créés...
  → 200 annonces créées...
  ...

Résumé:
  - 546 utilisateurs créés
  - 1092 annonces créées

Import terminé avec succès!
```

## 🔒 Sécurité

⚠️ **Important** : Ce script est destiné à un usage de développement/test. Pour la production :

1. Changez les mots de passe des utilisateurs créés
2. Vérifiez que les images téléchargées respectent les droits d'auteur
3. Assurez-vous que le scraping est autorisé par le site source

---

**Note** : Le script utilise des transactions pour garantir l'intégrité des données. En cas d'erreur, aucune donnée partielle ne sera enregistrée.

