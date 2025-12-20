# Solution Finale DNS LWS + Render

## 📋 Configuration Recommandée

### Étape 1 : Pointer @ vers LWS pour le SSL

Sur LWS, dans la section DNS :

1. **Ajoutez/modifiez l'enregistrement A pour @** :
   - **Type** : A
   - **Nom** : `@`
   - **Valeur** : `91.216.107.201` (IP serveur WEB LWS)
   - **TTL** : 6 heures

2. **Gardez le MX** (pour le mail) :
   - **Type** : MX
   - **Nom** : `@`
   - **Valeur** : `10 mail.ci-kiaba.com.`

3. **Gardez le CNAME pour www** :
   - **Type** : CNAME
   - **Nom** : `www`
   - **Valeur** : `kiaba-rencontre-oqhr.onrender.com.`

### Étape 2 : Configurer le Redirect HTTP sur LWS

Une fois que le domaine pointe vers LWS et que le SSL est activé :

1. Allez dans la section **"Redirect"** ou **"Redirection"** du panneau LWS
2. Configurez :
   - **Source** : `ci-kiaba.com` (sans www)
   - **Destination** : `https://www.ci-kiaba.com`
   - **Type** : Permanent (301)
   - **Avec SSL** : Oui

### Étape 3 : Configurer le domaine sur Render

1. Allez sur le dashboard Render
2. Sélectionnez votre service web (`kiaba-web`)
3. Allez dans **"Settings"** → **"Custom Domains"**
4. Ajoutez `www.ci-kiaba.com`
5. Render générera automatiquement un certificat SSL

## ✅ Résultat Final

- `ci-kiaba.com` → LWS (SSL) → Redirect vers `www.ci-kiaba.com` → Render ✅
- `www.ci-kiaba.com` → Render directement (SSL automatique) ✅
- Mail fonctionne (MX sur LWS) ✅
- SSL fonctionne sur les deux domaines ✅

## ⏱️ Propagation

Attendez 6-24 heures pour la propagation DNS complète.

## 🔍 Vérification

Après configuration :
- `https://ci-kiaba.com` → doit rediriger vers `https://www.ci-kiaba.com`
- `https://www.ci-kiaba.com` → doit afficher votre site Render
- Les deux doivent avoir un certificat SSL valide

---

**Note** : Cette configuration est standard et fonctionne parfaitement. Le domaine racine utilise LWS comme proxy/redirect, et www pointe directement vers Render.

