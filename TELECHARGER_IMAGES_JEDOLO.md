# Guide : Télécharger les Images depuis ci.jedolo.com

## 📋 Objectif

Télécharger les images depuis `ci.jedolo.com` et les utiliser dans les annonces créées.

## 🚀 Méthode 1 : Télécharger Localement puis Pousser

### 1. Télécharger les Images Localement

```bash
# Sur votre machine locale (avec Django installé)
python manage.py download_jedolo_images --max-images 100
```

Cela téléchargera les images dans `media/jedolo_images/`

### 2. Copier les Images dans le Repo

```bash
# Copier les images dans static/jedolo_images pour les inclure dans le repo
cp media/jedolo_images/* static/jedolo_images/
```

### 3. Ajouter au Git

```bash
git add static/jedolo_images/
git commit -m "Add: Images depuis ci.jedolo.com"
git push origin master
```

## 🚀 Méthode 2 : Télécharger Directement sur Render

### 1. Dans le Shell Render

```bash
# Télécharger les images
python manage.py download_jedolo_images --max-images 100
```

Les images seront téléchargées dans `media/jedolo_images/` sur Render.

### 2. Utiliser les Images

Le script `import_from_jedolo` utilisera automatiquement ces images.

## 📁 Structure des Dossiers

```
project/
  static/
    jedolo_images/     # Images dans le repo (recommandé)
      jedolo_1.jpg
      jedolo_2.jpg
      ...
  media/
    jedolo_images/     # Images téléchargées (non commitées)
      jedolo_1.jpg
      jedolo_2.jpg
      ...
```

## ✅ Utilisation

Une fois les images téléchargées, le script `import_from_jedolo` les utilisera automatiquement :

```bash
python manage.py import_from_jedolo --users 100 --ads 300
```

Le script cherchera les images dans :
1. `static/jedolo_images/` (priorité)
2. `media/jedolo_images/` (si static/ est vide)

## 🔍 Vérification

Pour vérifier que les images sont disponibles :

```bash
# Compter les images
ls static/jedolo_images/ | wc -l
# ou
ls media/jedolo_images/ | wc -l
```

## ⚠️ Notes

- Les images dans `media/` ne sont pas commitées (dans .gitignore)
- Les images dans `static/` sont commitées et disponibles sur Render
- Le script utilise jusqu'à 5 images par annonce
- Les images sont sélectionnées aléatoirement pour chaque annonce

---

**Recommandation** : Utilisez la Méthode 1 pour avoir les images dans le repo et disponibles sur Render automatiquement.

