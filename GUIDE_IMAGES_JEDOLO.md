# Guide : Où Mettre les Images pour les Annonces

## 📁 Dossier pour les Images

**Mettez toutes vos images dans ce dossier :**

```
static/jedolo_images/
```

## 📋 Étapes

### 1. Sur votre Machine Locale

1. **Allez dans le dossier du projet** :
   ```bash
   cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-maj
   ```

2. **Créez le dossier si nécessaire** :
   ```bash
   mkdir -p static/jedolo_images
   ```

3. **Copiez vos images dans ce dossier** :
   ```bash
   # Exemple : copier des images
   cp /chemin/vers/vos/images/* static/jedolo_images/
   ```

### 2. Nommage des Images

**Vous pouvez nommer les images comme vous voulez** :
- `image1.jpg`
- `photo_annonce.png`
- `jedolo_001.jpg`
- `annonce_1.webp`
- etc.

Le script les utilisera automatiquement et les renommera lors de l'import.

### 3. Formats Acceptés

- `.jpg` / `.jpeg`
- `.png`
- `.webp`
- `.gif`

### 4. Ajouter au Git

Une fois les images dans `static/jedolo_images/` :

```bash
git add static/jedolo_images/
git commit -m "Add: Images pour les annonces"
git push origin master
```

## ✅ Utilisation

Une fois les images dans `static/jedolo_images/`, le script `import_from_jedolo` les utilisera automatiquement :

```bash
python manage.py import_from_jedolo --users 100 --ads 300
```

Le script :
- ✅ Trouvera automatiquement toutes les images dans `static/jedolo_images/`
- ✅ Les assignera au hasard aux annonces (1-5 images par annonce)
- ✅ Les renommera automatiquement lors de l'import

## 📊 Nombre d'Images Recommandé

Pour 300 annonces avec 1-5 images chacune :
- **Minimum** : 300 images (1 par annonce)
- **Recommandé** : 500-1000 images (pour varier)

## 🔍 Vérification

Pour vérifier que les images sont bien dans le dossier :

```bash
ls static/jedolo_images/ | wc -l
```

## ⚠️ Important

- Les images dans `static/jedolo_images/` seront **commitées dans Git**
- Elles seront disponibles sur Render après le push
- Taille recommandée : < 5MB par image
- Le script utilisera jusqu'à 5 images par annonce

---

**Résumé** : Mettez toutes vos images dans `static/jedolo_images/` et le script les utilisera automatiquement !

