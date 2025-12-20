# Guide : Désactiver le Service Web LWS

## ✅ Configuration DNS Correcte

Votre configuration DNS est **correcte** :
- ✅ A `@` = `216.24.57.7` (Render)
- ✅ CNAME `www` = `kiaba-rencontre-oqhr.onrender.com` (Render)
- ✅ MX configuré pour le mail

## 🔴 Problème

LWS affiche toujours la page par défaut car un **service web/hébergement est activé** pour ce domaine.

## 🔍 Où Désactiver le Service Web LWS

### Option 1 : Section "Hébergement Web"

1. Dans le panneau LWS, cherchez une section **"Hébergement Web"** ou **"Web Hosting"**
2. Cherchez le domaine `ci-kiaba.com` dans la liste
3. Cliquez sur **"Désactiver"** ou **"Supprimer"** ou **"Suspendre"**

### Option 2 : Section "Services" ou "Mes Services"

1. Allez dans **"Mes Services"** ou **"Services"**
2. Cherchez un service web/hébergement pour `ci-kiaba.com`
3. Désactivez-le ou supprimez-le

### Option 3 : Section "Domaines" → "Gestion"

1. Allez dans la gestion du domaine `ci-kiaba.com`
2. Cherchez une section **"Hébergement"**, **"Service Web"**, ou **"Web Hosting"**
3. Cherchez un bouton **"Désactiver"**, **"Supprimer"**, ou **"Pas d'hébergement"**

### Option 4 : Contactez le Support LWS

Si vous ne trouvez pas l'option :

1. Ouvrez un **ticket de support** sur LWS
2. Demandez : **"Pouvez-vous désactiver le service web/hébergement pour le domaine ci-kiaba.com ? Je utilise un hébergement externe (Render)."**

## 📋 Ce qu'il faut Chercher

Sur le panneau LWS, cherchez :
- ❌ "Hébergement Web activé"
- ❌ "Service Web actif"
- ❌ "Hébergement mutualisé"
- ❌ "Web Hosting"
- ❌ Un indicateur vert/actif pour un service web

## ✅ Après Désactivation

Une fois le service web désactivé :

1. **Attendez 5-10 minutes** pour que les changements prennent effet
2. **Testez** : `https://ci-kiaba.com`
3. **Vous devriez voir** : La page d'âge (18+) puis votre site Django

## 🔍 Vérification

Pour vérifier si le service web est désactivé :

```bash
curl -I https://ci-kiaba.com
```

**Si le service web est désactivé**, vous devriez voir :
- `x-render-origin-server: gunicorn`
- `location: /age-gate/`

**Si le service web est encore activé**, vous verrez :
- `x-orig-rid: ...`
- `x-anubis-action: ...`
- Page HTML de LWS

## 💡 Note Importante

Le DNS est correct. Le problème est uniquement que LWS intercepte les requêtes HTTP/HTTPS avant qu'elles n'atteignent Render car un service web est activé.

Une fois désactivé, les requêtes passeront directement à Render via l'enregistrement A (`216.24.57.7`) et vous verrez votre site Django.

---

**Action Immédiate** : Cherchez la section "Hébergement Web" ou "Service Web" dans le panneau LWS et désactivez-le pour `ci-kiaba.com`.

