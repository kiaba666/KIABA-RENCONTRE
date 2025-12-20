# Configuration DNS LWS - Solution Finale

## ✅ Situation Actuelle

Render gère déjà les deux domaines avec SSL :
- `www.ci-kiaba.com` → redirects to `ci-kiaba.com` ✅
- `ci-kiaba.com` → Domain Verified, Certificate Issued ✅

## 🔧 Configuration DNS sur LWS

Puisque Render utilise Cloudflare CDN, les IPs peuvent changer. Voici les IPs actuelles :

**IPs de Render (via Cloudflare)** :
- `216.24.57.7`
- `216.24.57.251`

### Option 1 : Utiliser les IPs de Render (Temporaire)

Sur LWS, dans la section DNS :

1. **Modifiez l'enregistrement A pour @** :
   - **Type** : A
   - **Nom** : `@`
   - **Valeur** : `216.24.57.7` (ou `216.24.57.251`)
   - **TTL** : 6 heures (ou moins pour changement rapide)

2. **Gardez le MX** (pour le mail) :
   - **Type** : MX
   - **Nom** : `@`
   - **Valeur** : `10 mail.ci-kiaba.com.`

3. **Gardez le CNAME pour www** :
   - **Type** : CNAME
   - **Nom** : `www`
   - **Valeur** : `kiaba-rencontre-oqhr.onrender.com.`

⚠️ **Attention** : Ces IPs peuvent changer car Render utilise Cloudflare. Si le site ne fonctionne plus, vérifiez les IPs avec :
```bash
nslookup kiaba-rencontre-oqhr.onrender.com
```

### Option 2 : Utiliser Cloudflare (Recommandé - Plus stable)

1. Créez un compte gratuit sur https://cloudflare.com
2. Ajoutez votre domaine `ci-kiaba.com`
3. Cloudflare vous donnera des nameservers (ex: `ns1.cloudflare.com`)
4. Sur LWS, changez les nameservers vers ceux de Cloudflare
5. Sur Cloudflare, configurez :
   - `@` → CNAME (proxied) vers `kiaba-rencontre-oqhr.onrender.com`
   - `www` → CNAME (proxied) vers `kiaba-rencontre-oqhr.onrender.com`
   - `@` → MX pour le mail (10 mail.ci-kiaba.com)

Cloudflare supporte CNAME flattening, donc vous pouvez avoir CNAME + MX sur @.

## ✅ Vérification

Après configuration (attendre 6-24h pour propagation) :
- `https://ci-kiaba.com` → doit pointer vers Render
- `https://www.ci-kiaba.com` → doit pointer vers Render
- Les deux doivent avoir le certificat SSL de Render

## 🔍 Test

Testez avec :
```bash
curl -I https://ci-kiaba.com
```

Vous devriez voir les headers de Render.

---

**Recommandation** : Utilisez Cloudflare pour une solution plus stable et professionnelle.

