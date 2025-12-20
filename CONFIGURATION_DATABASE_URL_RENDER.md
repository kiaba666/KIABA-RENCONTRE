# Configuration DATABASE_URL sur Render

## ✅ Format Correct de DATABASE_URL

La `DATABASE_URL` que vous avez fournie est incomplète. Voici le format correct :

### ❌ Format Incomplet (ce que vous avez fourni)
```
postgresql://kiaba_db_wzbz_user:GIC0OwgP0ACv90JSg1EH19Hre1Ndg1ir@dpg-d53940khg0os738mrqq0-a/kiaba_db_wzbz_8ruc
```

### ✅ Format Complet (à utiliser)
```
postgresql://kiaba_db_wzbz_user:GIC0OwgP0ACv90JSg1EH19Hre1Ndg1ir@dpg-d53940khg0os738mrqq0-a.oregon-postgres.render.com:5432/kiaba_db_wzbz_8ruc?sslmode=prefer
```

## 📋 Structure de DATABASE_URL

Format général :
```
postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]?[OPTIONS]
```

Votre configuration :
- **USER** : `kiaba_db_wzbz_user`
- **PASSWORD** : `GIC0OwgP0ACv90JSg1EH19Hre1Ndg1ir`
- **HOST** : `dpg-d53940khg0os738mrqq0-a.oregon-postgres.render.com` (complet avec domaine)
- **PORT** : `5432`
- **DATABASE** : `kiaba_db_wzbz_8ruc`
- **OPTIONS** : `sslmode=prefer` (pour SSL)

## 🎯 Étapes pour Configurer sur Render

### 1. Aller dans le Dashboard Render

1. Allez sur https://dashboard.render.com
2. Ouvrez votre service web (`kiaba-web`)

### 2. Supprimer les Anciennes Variables

**IMPORTANT** : Supprimez ces variables d'environnement pour éviter les conflits :
- ❌ `POSTGRES_HOST`
- ❌ `POSTGRES_DB`
- ❌ `POSTGRES_USER`
- ❌ `POSTGRES_PASSWORD`
- ❌ `POSTGRES_PORT`
- ❌ `DB_ENGINE`

### 3. Ajouter DATABASE_URL

1. Allez dans **"Environment"**
2. Cliquez sur **"Add Environment Variable"**
3. Ajoutez :
   - **Key** : `DATABASE_URL`
   - **Value** : `postgresql://kiaba_db_wzbz_user:GIC0OwgP0ACv90JSg1EH19Hre1Ndg1ir@dpg-d53940khg0os738mrqq0-a.oregon-postgres.render.com:5432/kiaba_db_wzbz_8ruc?sslmode=prefer`

### 4. Alternative : Lier la Base de Données

**Méthode recommandée** : Au lieu de créer manuellement `DATABASE_URL`, vous pouvez :

1. Dans votre service web, allez dans **"Environment"**
2. Cliquez sur **"Link Database"**
3. Sélectionnez votre base de données PostgreSQL (`kiaba_db_wzbz_8ruc`)
4. Render créera automatiquement `DATABASE_URL` avec le bon format

**Avantage** : Render gère automatiquement les mises à jour si la base de données change.

## ✅ Vérification

Après avoir ajouté `DATABASE_URL` :

1. ✅ Le service va redéployer automatiquement
2. ✅ Vérifiez les logs pour confirmer que la connexion fonctionne
3. ✅ Le code dans `settings.py` détectera automatiquement `DATABASE_URL` et l'utilisera

## 🔍 Code dans settings.py

Le code vérifie automatiquement `DATABASE_URL` :

```python
database_url = os.environ.get("DATABASE_URL")

if database_url:
    # Utiliser DATABASE_URL si fourni
    DATABASES = {
        "default": env.db("DATABASE_URL")
    }
    DATABASES["default"]["OPTIONS"]["sslmode"] = "prefer"
```

## 📝 Notes Importantes

1. **Sécurité** : Le mot de passe est dans l'URL. C'est normal pour `DATABASE_URL`, mais assurez-vous que seules les personnes autorisées ont accès au dashboard Render.

2. **sslmode=prefer** : Ajouté dans l'URL pour éviter les problèmes SSL. Le code dans `settings.py` l'ajoute aussi dans `OPTIONS` pour être sûr.

3. **Supprimer les anciennes variables** : C'est important pour éviter que Django utilise les mauvaises variables.

---

**Format final à copier-coller dans Render** :
```
postgresql://kiaba_db_wzbz_user:GIC0OwgP0ACv90JSg1EH19Hre1Ndg1ir@dpg-d53940khg0os738mrqq0-a.oregon-postgres.render.com:5432/kiaba_db_wzbz_8ruc?sslmode=prefer
```

