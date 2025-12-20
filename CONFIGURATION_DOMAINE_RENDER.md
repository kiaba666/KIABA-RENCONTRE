# Configuration du Domaine ci-kiaba.com pour Render

## 📋 Situation Actuelle

Vous avez acheté le domaine `ci-kiaba.com` sur LWS et vous l'avez connecté. 

## ⚠️ Important : Le domaine doit pointer vers Render, PAS vers GitHub

### Configuration DNS sur LWS

Le domaine `ci-kiaba.com` doit pointer vers votre service Render, pas vers GitHub Pages.

### Étapes pour configurer le domaine sur Render

1. **Sur le dashboard Render** :
   - Allez dans votre service web (`kiaba-web`)
   - Cliquez sur "Settings"
   - Dans la section "Custom Domains", ajoutez `ci-kiaba.com`
   - Render vous donnera un enregistrement CNAME ou A à configurer

2. **Sur LWS (votre registrar)** :
   - Allez dans la gestion DNS de votre domaine
   - Ajoutez l'enregistrement CNAME ou A fourni par Render
   - Pour `ci-kiaba.com` → CNAME vers l'URL Render (ex: `kiaba-web.onrender.com`)
   - Pour `www.ci-kiaba.com` → CNAME vers l'URL Render

### Vérification

Une fois configuré, vérifiez que :
- `ci-kiaba.com` pointe vers Render (pas GitHub)
- Le certificat SSL est automatiquement généré par Render
- L'application est accessible via `https://ci-kiaba.com`

## 🔍 Le problème SSL PostgreSQL est INDÉPENDANT du domaine

Le problème de connexion SSL à PostgreSQL est un problème de **configuration de base de données**, pas de domaine. Le domaine n'affecte pas la connexion à la base de données.

---

**Note** : Si vous avez connecté le domaine à GitHub au lieu de Render, c'est pour ça que le site ne fonctionne pas. Le domaine doit pointer vers Render.

