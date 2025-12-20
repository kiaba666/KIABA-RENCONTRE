# Exécuter l'Import sur Render

## 🚀 Méthode 1 : Via le Shell Render (Recommandé)

### Étapes :

1. **Allez sur votre dashboard Render** : https://dashboard.render.com
2. **Ouvrez votre service web** (`kiaba-web`)
3. **Allez dans l'onglet "Shell"**
4. **Exécutez la commande** :

```bash
python manage.py import_from_jedolo --users 546 --ads-per-user 2
```

### Avantages :

- ✅ Toutes les dépendances sont déjà installées
- ✅ Accès direct à la base de données
- ✅ Pas besoin de configuration locale

---

## 🖥️ Méthode 2 : Via le Terminal Local (Si vous avez un environnement virtuel)

### Créer un environnement virtuel :

```bash
cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-maj
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Exécuter le script :

```bash
python manage.py import_from_jedolo --users 546 --ads-per-user 2
```

---

## 📋 Commandes Disponibles

```bash
# Créer 546 utilisateurs avec 2 annonces chacun (défaut)
python manage.py import_from_jedolo

# Créer 546 utilisateurs avec 2-5 annonces chacun
python manage.py import_from_jedolo --users 546

# Créer 100 utilisateurs avec 3 annonces chacun
python manage.py import_from_jedolo --users 100 --ads-per-user 3

# Créer 546 utilisateurs avec 2-6 annonces chacun
python manage.py import_from_jedolo --users 546 --ads-per-user 2 --max-ads 6
```

---

## ⚠️ Notes Importantes

- Le script peut prendre **plusieurs minutes** à s'exécuter (scraping + création)
- Les images seront téléchargées et stockées dans `media/ads/`
- Tous les utilisateurs auront le mot de passe : `password123`
- Toutes les annonces seront automatiquement approuvées

---

## 🔍 Vérification

Après l'exécution, vérifiez :

1. **Nombre d'utilisateurs** :

   ```bash
   python manage.py shell -c "from accounts.models import CustomUser; print(CustomUser.objects.count())"
   ```

2. **Nombre d'annonces** :

   ```bash
   python manage.py shell -c "from ads.models import Ad; print(Ad.objects.count())"
   ```

3. **Vérifier sur le site** : Allez sur `https://ci-kiaba.com` et vérifiez que les annonces s'affichent

---

**Recommandation** : Utilisez la **Méthode 1** (Shell Render) car c'est plus simple et toutes les dépendances sont déjà installées.
