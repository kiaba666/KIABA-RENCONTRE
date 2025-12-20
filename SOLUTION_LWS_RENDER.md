# Solution LWS + Render - Configuration Finale

## ✅ Configuration DNS sur LWS

Puisque vous voulez rester avec LWS et Render, voici la configuration exacte :

### Enregistrements DNS à configurer sur LWS

1. **Enregistrement A pour @ (racine)** :

   - **Type** : A
   - **Nom** : `@` (ou laissez vide)
   - **Valeur** : `216.24.57.7` (IP de Render via Cloudflare)
   - **TTL** : 6 heures

   ⚠️ **Note** : Cette IP peut changer. Si le site ne fonctionne plus, vérifiez avec :

   ```bash
   nslookup kiaba-rencontre-oqhr.onrender.com
   ```

2. **Enregistrement MX pour @ (mail)** :

   - **Type** : MX
   - **Nom** : `@`
   - **Valeur** : `10 mail.ci-kiaba.com.`
   - **TTL** : 24 heures

   ✅ **Déjà configuré** - Ne pas modifier

3. **Enregistrement CNAME pour www** :

   - **Type** : CNAME
   - **Nom** : `www`
   - **Valeur** : `kiaba-rencontre-oqhr.onrender.com.` (avec le point final)
   - **TTL** : 24 heures

   ✅ **Déjà configuré** - Vérifier qu'il pointe bien vers Render

## 📋 Configuration Complète sur LWS

```
Type    Nom    Valeur                                    TTL
A       @      216.24.57.7                               6h
MX      @      10 mail.ci-kiaba.com.                     24h
CNAME   www    kiaba-rencontre-oqhr.onrender.com.        24h
```

## ✅ Résultat

- `ci-kiaba.com` → IP Render (216.24.57.7) → Render gère le SSL ✅
- `www.ci-kiaba.com` → CNAME vers Render → Render gère le SSL ✅
- Mail fonctionne (MX sur LWS) ✅

## 🔍 Vérification sur Render

Sur Render, vérifiez que les deux domaines sont bien configurés :

- `ci-kiaba.com` → Domain Verified, Certificate Issued ✅
- `www.ci-kiaba.com` → Domain Verified, Certificate Issued ✅

## ⚠️ Important : Si l'IP change

Si Render change son IP (ce qui peut arriver), vous devrez :

1. Vérifier la nouvelle IP :
   ```bash
   nslookup kiaba-rencontre-oqhr.onrender.com
   ```
2. Mettre à jour l'enregistrement A pour @ sur LWS avec la nouvelle IP

## 🚀 Prochaines Étapes

1. **Sur LWS** : Modifiez l'enregistrement A pour `@` → `216.24.57.7`
2. **Attendez 6-24 heures** pour la propagation DNS
3. **Testez** : `https://ci-kiaba.com` et `https://www.ci-kiaba.com`

---

**Note** : Cette solution fonctionne avec LWS et Render. Le seul inconvénient est que si Render change son IP, vous devrez mettre à jour l'enregistrement A.
