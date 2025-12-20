# Solution DNS LWS - Conflit CNAME/MX

## 🔴 Problème

LWS refuse le CNAME pour `@` car il y a déjà un enregistrement **MX** pour `@` :
```
MX  @  10  mail.ci-kiaba.com.
```

**Règle DNS** : Vous ne pouvez pas avoir à la fois un CNAME et un MX (ou A) pour le même nom.

## ✅ Solution : Redirect HTTP sur LWS

Puisque vous avez besoin du MX pour le mail, utilisez un **redirect HTTP** au lieu d'un CNAME.

### Étapes sur LWS

1. **Ne modifiez PAS le DNS** (gardez le MX pour le mail)
2. **Allez dans la section "Redirect" ou "Redirection"** du panneau LWS
3. **Configurez une redirection HTTP** :
   - **Source** : `ci-kiaba.com` (sans www)
   - **Destination** : `https://www.ci-kiaba.com`
   - **Type** : Permanent (301) ou Temporaire (302)
   - **Avec SSL** : Oui

### Alternative : Vérifier si LWS supporte ALIAS/ANAME

Certains DNS modernes supportent ALIAS/ANAME qui permet d'avoir MX + ALIAS. Vérifiez si LWS propose cette option.

## 📋 Configuration DNS Finale

**Gardez tel quel** :
```
MX      @    10    mail.ci-kiaba.com.          (pour le mail)
CNAME   www        kiaba-rencontre-oqhr.onrender.com.  (déjà OK)
```

**Ajoutez un redirect HTTP** :
```
ci-kiaba.com → https://www.ci-kiaba.com (301 redirect)
```

## ✅ Résultat

- `ci-kiaba.com` → redirect vers `www.ci-kiaba.com` → Render ✅
- `www.ci-kiaba.com` → Render directement ✅
- Mail fonctionne toujours (MX conservé) ✅

## 🔍 Vérification

Après configuration du redirect :
- `http://ci-kiaba.com` → redirige vers `https://www.ci-kiaba.com`
- `https://ci-kiaba.com` → redirige vers `https://www.ci-kiaba.com`
- Les deux doivent fonctionner avec SSL

---

**Note** : Cette solution est courante et fonctionne parfaitement. Beaucoup de sites utilisent cette approche (ex: GitHub Pages, Netlify, etc.)

