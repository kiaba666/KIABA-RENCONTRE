# Guide : Créer une Base de Données PostgreSQL sur Render

## 📋 Étapes pour Créer PostgreSQL sur Render

### 1. Aller sur le Dashboard Render

1. Allez sur https://dashboard.render.com
2. Connectez-vous avec votre compte

### 2. Créer une Nouvelle Base de Données

1. Cliquez sur **"New +"** en haut à droite
2. Sélectionnez **"PostgreSQL"**
3. Configurez la base de données :
   - **Name** : `kiaba-db` (ou un nom de votre choix)
   - **Database** : `kiaba_db_wzbz` (ou le nom que vous voulez)
   - **User** : `kiaba_db_wzbz_user` (ou le nom que vous voulez)
   - **Region** : Choisissez la même région que votre service web (Frankfurt)
   - **PostgreSQL Version** : 15 (recommandé)
   - **Plan** : Free (pour commencer)

4. Cliquez sur **"Create Database"**

### 3. Récupérer les Informations de Connexion

Une fois la base créée, Render vous donnera :

1. **Internal Database URL** (pour connexions internes) :
   - Format : `postgres://user:password@host-internal:5432/dbname`
   - Host se termine par `-a.oregon-postgres.render.com`

2. **External Database URL** (pour connexions externes) :
   - Format : `postgres://user:password@host-external:5432/dbname`
   - Host se termine par `.oregon-postgres.render.com`

3. **Informations individuelles** :
   - **Host** : `dpg-xxxxx.oregon-postgres.render.com`
   - **Port** : `5432`
   - **Database** : Le nom de la base
   - **User** : Le nom d'utilisateur
   - **Password** : Le mot de passe (à copier immédiatement)

### 4. Mettre à Jour render.yaml

Une fois que vous avez les informations, mettez à jour `render.yaml` :

```yaml
envVars:
  - key: POSTGRES_DB
    value: "VOTRE_NOM_DE_BASE"
  - key: POSTGRES_USER
    value: "VOTRE_UTILISATEUR"
  - key: POSTGRES_PASSWORD
    value: "VOTRE_MOT_DE_PASSE"
  - key: POSTGRES_HOST
    value: "VOTRE_HOST.oregon-postgres.render.com"
  - key: POSTGRES_PORT
    value: "5432"
```

### 5. Alternative : Utiliser DATABASE_URL

Render peut aussi fournir une variable `DATABASE_URL` automatiquement. Si vous utilisez cette option :

1. Sur Render, dans votre service web
2. Allez dans **"Environment"**
3. Cliquez sur **"Link Database"**
4. Sélectionnez votre base de données PostgreSQL
5. Render ajoutera automatiquement `DATABASE_URL`

Ensuite, dans `settings.py`, vous pouvez utiliser :
```python
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
```

## ✅ Vérification

Après création de la base de données :

1. ✅ La base de données apparaît dans votre dashboard Render
2. ✅ Vous avez les informations de connexion
3. ✅ Vous pouvez tester la connexion depuis Render (section "Connect")

## 🔍 Prochaines Étapes

1. Créer la base de données PostgreSQL sur Render
2. Mettre à jour `render.yaml` avec les nouvelles informations
3. Pousser les changements vers GitHub
4. Render redéploiera automatiquement avec la bonne configuration

---

**Note** : Le plan Free de Render PostgreSQL a des limitations (90 jours, puis suppression). Pour la production, envisagez un plan payant.

