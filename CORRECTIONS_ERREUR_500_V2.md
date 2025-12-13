# Corrections supplémentaires pour l'erreur 500 - Version 2

## Problèmes identifiés dans les logs

1. **Les migrations ne sont pas exécutées** : Dans les logs, on voit seulement `collectstatic` mais pas `migrate`
2. **Accès à la base de données pendant l'initialisation** : Le warning indique que `core/apps.py` accède à la base de données dans `ready()`
3. **Le Site Django n'est peut-être pas créé** : Si les migrations ne sont pas exécutées, le Site avec `SITE_ID=1` n'existe pas

## Corrections appliquées

### 1. Script de démarrage robuste (`start.sh`)

Création d'un script de démarrage qui :
- ✅ Exécute les migrations de manière explicite
- ✅ Crée le Site Django après les migrations
- ✅ Vérifie la configuration Django
- ✅ Affiche des logs détaillés pour le débogage
- ✅ Gère les erreurs correctement

### 2. Correction de `core/apps.py`

- ✅ Suppression de l'appel immédiat à la base de données dans `ready()`
- ✅ Utilisation uniquement du signal `post_migrate` pour créer/mettre à jour le Site
- ✅ Vérification de la connexion à la base de données avant d'accéder aux modèles

### 3. Mise à jour de `render.yaml`

- ✅ Utilisation du script `start.sh` au lieu d'une commande directe
- ✅ Le script garantit que les migrations sont exécutées avant le démarrage

## Fichiers modifiés

1. `core/apps.py` - Correction de l'accès à la base de données
2. `start.sh` - Nouveau script de démarrage (créé)
3. `render.yaml` - Mise à jour du startCommand

## Prochaines étapes

1. **Commiter et pousser les changements** :
```bash
git add .
git commit -m "Fix: Ajouter script de démarrage robuste et corriger core/apps.py"
git push origin main
```

2. **Vérifier les logs Render** après le déploiement :
   - Vous devriez voir "Step 1: Running database migrations..."
   - Vous devriez voir "Step 2: Setting up Django Site..."
   - Vous devriez voir "✓ Site configured: ci-kiaba.com"

3. **Tester l'application** sur https://ci-kiaba.com

## Ce qui devrait se passer maintenant

1. Le script `start.sh` s'exécute au démarrage
2. Les migrations sont exécutées automatiquement
3. Le Site Django est créé avec le bon domaine
4. Gunicorn démarre avec des logs détaillés
5. L'erreur 500 devrait être résolue

## Si l'erreur persiste

Vérifiez les logs Render pour voir :
- Si les migrations s'exécutent correctement
- Si le Site est créé
- S'il y a des erreurs de connexion à la base de données
- Les logs Gunicorn pour voir l'erreur exacte

