# Solution : Désactiver la Redirection Web LWS

## 🔍 Analyse du Panneau LWS

Vous avez la **formule "domaine"** qui inclut :
- ✅ Espace Web: 1 Go
- ✅ Un service web basique qui affiche une page par défaut

## ✅ Solution : Section "Redirection web"

Dans le menu de gauche, vous avez **"Redirection web"**. C'est là qu'il faut aller !

### Étapes :

1. **Cliquez sur "Redirection web"** dans le menu de gauche
2. **Vérifiez s'il y a une redirection active** vers la page par défaut LWS
3. **Désactivez la redirection** ou configurez-la pour pointer vers Render

### Options Possibles dans "Redirection web" :

- **Désactiver la redirection** : Si une redirection est active, désactivez-la
- **Configurer une redirection vers Render** : Redirigez vers `https://kiaba-rencontre-oqhr.onrender.com`
- **Aucune redirection** : Laissez vide pour que le DNS gère directement

## 🎯 Configuration Recommandée

### Option 1 : Désactiver la Redirection (Recommandé)

1. Allez dans **"Redirection web"**
2. **Désactivez** toute redirection active
3. Laissez le domaine pointer directement via DNS vers Render (`216.24.57.7`)

### Option 2 : Rediriger vers Render

Si vous ne pouvez pas désactiver complètement :

1. Allez dans **"Redirection web"**
2. Configurez une redirection **HTTP 301** (permanente) :
   - **Source** : `ci-kiaba.com`
   - **Destination** : `https://kiaba-rencontre-oqhr.onrender.com`
   - **Type** : Permanent (301)

⚠️ **Note** : Cette option n'est pas idéale car elle crée une redirection supplémentaire, mais elle peut fonctionner.

## 📋 Checklist

- [ ] Aller dans "Redirection web"
- [ ] Vérifier s'il y a une redirection active
- [ ] Désactiver la redirection ou la configurer vers Render
- [ ] Attendre 5-10 minutes
- [ ] Tester `https://ci-kiaba.com`

## 🔍 Autres Options à Vérifier

Si "Redirection web" ne résout pas le problème, vérifiez aussi :

1. **"Sous domaines"** : Vérifiez qu'aucun sous-domaine ne redirige vers la page par défaut
2. **"Gestionnaire de fichiers"** : Vérifiez qu'il n'y a pas de fichier `index.html` qui affiche la page par défaut
3. **Contactez le support LWS** : Demandez de désactiver le service web pour ce domaine

## 💡 Pourquoi ça se Passe

Avec la formule "domaine", LWS active un service web basique qui :
- Affiche une page par défaut si aucun site n'est configuré
- Peut avoir une redirection active vers cette page par défaut

En désactivant la redirection ou en la configurant correctement, les requêtes passeront directement via DNS vers Render.

---

**Action Immédiate** : Cliquez sur **"Redirection web"** dans le menu de gauche et désactivez toute redirection active.

