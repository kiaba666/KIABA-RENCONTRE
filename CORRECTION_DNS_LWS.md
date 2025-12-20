# Correction DNS pour ci-kiaba.com sur LWS

## 🔴 Problème Identifié

Dans votre configuration DNS actuelle :
- ✅ `www.ci-kiaba.com` → CNAME vers `kiaba-rencontre-oqhr.onrender.com` (CORRECT)
- ❌ `ci-kiaba.com` (racine @) → A vers `216.24.57.1` (IP LWS, INCORRECT)

Le domaine racine pointe vers LWS au lieu de Render !

## ✅ Solution : Configurer le CNAME pour @

### Option 1 : CNAME pour @ (Recommandé)

Sur LWS, modifiez l'enregistrement DNS :

1. **Supprimez** l'enregistrement A pour `@` avec la valeur `216.24.57.1`
2. **Ajoutez** un enregistrement CNAME :
   - **Type** : CNAME
   - **Nom** : `@` (ou laissez vide pour la racine)
   - **Valeur** : `kiaba-rencontre-oqhr.onrender.com.` (avec le point à la fin)
   - **TTL** : 6 heures

### Option 2 : Si LWS ne supporte pas CNAME pour @

Si LWS ne permet pas CNAME sur la racine (@), vous avez deux options :

#### A. Utiliser un redirect sur LWS
Configurez un redirect HTTP de `ci-kiaba.com` vers `www.ci-kiaba.com` sur le panneau LWS.

#### B. Vérifier l'IP de Render (non recommandé)
Render utilise des noms de domaine dynamiques, donc utiliser une IP fixe n'est pas recommandé.

## 📋 Configuration DNS Finale Recommandée

```
Type    Nom    Valeur                                    TTL
A       @      (SUPPRIMER - remplacer par CNAME)        
CNAME   @      kiaba-rencontre-oqhr.onrender.com.        6h
CNAME   www    kiaba-rencontre-oqhr.onrender.com.        24h (déjà OK)
```

## 🔍 Vérification sur Render

1. Allez sur le dashboard Render
2. Sélectionnez votre service web
3. Allez dans "Settings" → "Custom Domains"
4. Vérifiez que `ci-kiaba.com` et `www.ci-kiaba.com` sont ajoutés
5. Render générera automatiquement un certificat SSL pour les deux domaines

## ⏱️ Propagation DNS

Après modification, attendez 6-24 heures pour la propagation DNS complète.

## ✅ Vérification

Une fois configuré, testez :
- `https://ci-kiaba.com` → doit pointer vers Render
- `https://www.ci-kiaba.com` → doit pointer vers Render
- Les deux doivent avoir un certificat SSL valide

---

**Note** : Le problème SSL PostgreSQL est INDÉPENDANT de cette configuration DNS. C'est un problème de connexion à la base de données qui doit être résolu séparément.

