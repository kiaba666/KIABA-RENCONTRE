# Solution : ci-kiaba.com n'affiche pas le site

## ✅ Diagnostic

Les tests montrent que :
- ✅ `ci-kiaba.com` pointe vers Render (`216.24.57.7`)
- ✅ HTTPS fonctionne et redirige vers `/age-gate/` (page d'âge du site)
- ✅ HTTP redirige vers HTTPS
- ✅ Le site fonctionne sur `https://kiaba-rencontre-oqhr.onrender.com`

## 🔴 Problème

Vous voyez la page par défaut de LWS au lieu de votre site Django.

## 🔍 Causes Possibles

1. **Cache DNS local** : Votre navigateur/ordinateur a mis en cache l'ancienne IP
2. **Page par défaut LWS** : LWS affiche une page par défaut avant que la requête n'atteigne Render
3. **Propagation DNS incomplète** : Certains serveurs DNS n'ont pas encore mis à jour

## ✅ Solutions

### Solution 1 : Vider le Cache DNS (Recommandé)

**Sur macOS** :
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**Sur Windows** :
```cmd
ipconfig /flushdns
```

**Sur Linux** :
```bash
sudo systemd-resolve --flush-caches
# ou
sudo service network-manager restart
```

### Solution 2 : Tester en Navigation Privée

1. Ouvrez un navigateur en **mode navigation privée/incognito**
2. Allez sur `https://ci-kiaba.com`
3. Vous devriez voir votre site Django

### Solution 3 : Vérifier la Configuration LWS

Sur LWS, vérifiez qu'il n'y a pas :
- ❌ Une page par défaut activée
- ❌ Une redirection HTTP vers une page LWS
- ❌ Un service web LWS activé pour ce domaine

**Action** : Désactivez tout service web LWS pour `ci-kiaba.com` si activé.

### Solution 4 : Utiliser un autre DNS

Testez avec un autre serveur DNS :
- Google DNS : `8.8.8.8` et `8.8.4.4`
- Cloudflare DNS : `1.1.1.1` et `1.0.0.1`

**Sur macOS** :
1. Préférences Système → Réseau
2. Avancé → DNS
3. Ajoutez `8.8.8.8` et `8.8.4.4`
4. Appliquez

### Solution 5 : Vérifier sur Render

Sur Render, vérifiez que :
1. Le domaine `ci-kiaba.com` est bien dans "Custom Domains"
2. Le statut est "Domain Verified" ✅
3. Le certificat SSL est "Certificate Issued" ✅

## 🧪 Tests à Effectuer

### Test 1 : Vérifier avec curl
```bash
curl -I https://ci-kiaba.com
```
**Résultat attendu** : `HTTP/2 302` avec `location: /age-gate/`

### Test 2 : Vérifier le DNS
```bash
nslookup ci-kiaba.com
```
**Résultat attendu** : `216.24.57.7`

### Test 3 : Tester directement
Ouvrez `https://ci-kiaba.com` dans un navigateur en navigation privée.

## 📋 Checklist

- [ ] Cache DNS vidé
- [ ] Testé en navigation privée
- [ ] Vérifié qu'aucun service web LWS n'est activé
- [ ] Vérifié la configuration sur Render
- [ ] Attendu 6-24h pour propagation DNS complète

## 🎯 Action Immédiate

1. **Videz le cache DNS** (commande ci-dessus)
2. **Testez en navigation privée** : `https://ci-kiaba.com`
3. **Si ça ne fonctionne pas** : Vérifiez sur LWS qu'aucun service web n'est activé pour ce domaine

## 💡 Note Importante

Le site **fonctionne** sur Render. Le problème est uniquement lié au cache DNS ou à une configuration LWS. Une fois le cache vidé et testé en navigation privée, vous devriez voir votre site Django.

---

**Si le problème persiste après avoir vidé le cache et testé en navigation privée**, contactez le support LWS pour vérifier qu'aucun service web n'est activé pour `ci-kiaba.com`.

