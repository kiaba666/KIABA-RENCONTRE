# Configuration IP Render sur LWS

## 🔍 IPs de Render pour votre Service

Votre service Render utilise Cloudflare, qui peut avoir plusieurs IPs :

### IPs Trouvées
- `216.24.57.7` (principale)
- `216.24.57.251` (secondaire)

## ✅ Configuration Recommandée sur LWS

### Option 1 : Utiliser l'IP Principale (Recommandé)

**Enregistrement A pour @** :
- **Type** : A
- **Nom** : `@` (ou vide)
- **Valeur** : `216.24.57.7`
- **TTL** : 6 heures

### Option 2 : Utiliser le CNAME (Meilleure Solution)

Au lieu d'utiliser une IP (qui peut changer), utilisez un CNAME :

**Enregistrement CNAME pour @** :
- **Type** : CNAME
- **Nom** : `@`
- **Valeur** : `kiaba-rencontre-oqhr.onrender.com.` (avec le point final)

⚠️ **Note** : Certains registrars (comme LWS) ne permettent pas de CNAME pour `@` si des enregistrements MX existent. Dans ce cas, utilisez l'Option 1.

## 📋 Configuration Complète sur LWS

```
Type    Nom    Valeur                                    TTL
A       @      216.24.57.7                               6h
CNAME   www    kiaba-rencontre-oqhr.onrender.com.        24h
MX      @      10 mail.ci-kiaba.com.                     24h
```

## ⚠️ Important : Désactiver le Service Web LWS

**CRUCIAL** : Même si vous configurez l'IP correctement, vous devez **désactiver le service web LWS** pour ce domaine, sinon LWS continuera d'intercepter les requêtes.

### Étapes :
1. LWS Panel → Gestion du domaine `ci-kiaba.com`
2. Section "Hébergement Web" ou "Service Web"
3. **Désactiver** le service web
4. Sauvegarder

## 🔄 Si l'IP Change

Si Render change son IP (ce qui peut arriver avec Cloudflare) :

1. **Vérifiez la nouvelle IP** :
   ```bash
   dig +short kiaba-rencontre-oqhr.onrender.com
   ```

2. **Mettez à jour l'enregistrement A** sur LWS avec la nouvelle IP

## 🎯 Pourquoi Utiliser l'IP au Lieu du CNAME pour @

- ✅ Compatible avec les enregistrements MX (mail)
- ✅ Fonctionne même si LWS ne permet pas CNAME pour @
- ⚠️ Nécessite une mise à jour manuelle si l'IP change

## 💡 Alternative : Utiliser www uniquement

Si vous ne pouvez pas faire fonctionner `ci-kiaba.com` (sans www) :

1. Configurez uniquement `www.ci-kiaba.com` avec CNAME vers Render
2. Configurez une redirection HTTP 301 sur LWS de `ci-kiaba.com` vers `www.ci-kiaba.com`

---

**Action Immédiate** :
1. Désactiver le service web LWS pour `ci-kiaba.com`
2. Configurer l'enregistrement A pour `@` = `216.24.57.7`
3. Attendre 5-10 minutes
4. Tester `https://ci-kiaba.com`

