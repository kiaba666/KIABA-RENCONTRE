# Solution : Pointer directement vers Render

## ✅ Bonne Nouvelle

Render gère déjà les deux domaines avec SSL :
- `www.ci-kiaba.com` → redirects to `ci-kiaba.com`
- `ci-kiaba.com` → Domain Verified, Certificate Issued

**Vous n'avez PAS besoin de redirect sur LWS !**

## 🔧 Configuration DNS sur LWS

Puisque Render gère déjà `ci-kiaba.com` avec SSL, vous devez pointer le DNS directement vers Render.

### Option 1 : Utiliser l'IP de Render (si disponible)

Render ne fournit généralement pas d'IP fixe, mais vous pouvez utiliser leur service de DNS.

### Option 2 : Utiliser un service DNS externe (Recommandé)

Utilisez Cloudflare (gratuit) ou un autre service DNS qui supporte ALIAS/ANAME :

1. **Transférez la gestion DNS vers Cloudflare** (gratuit)
2. Configurez :
   - `@` → ALIAS vers `kiaba-rencontre-oqhr.onrender.com`
   - `www` → CNAME vers `kiaba-rencontre-oqhr.onrender.com`
   - `@` → MX pour le mail (10 mail.ci-kiaba.com)

### Option 3 : Solution hybride avec LWS

Si vous devez garder LWS pour le DNS :

1. **Sur LWS, modifiez l'enregistrement A pour @** :
   - **Type** : A
   - **Nom** : `@`
   - **Valeur** : Trouvez l'IP de Render (voir ci-dessous)

2. **Pour trouver l'IP de Render** :
   ```bash
   nslookup kiaba-rencontre-oqhr.onrender.com
   ```
   Ou utilisez un outil en ligne : https://www.whatsmydns.net/

3. **Problème** : Render utilise des IPs dynamiques, donc cette solution n'est pas idéale.

## ✅ Solution Recommandée : Cloudflare

1. Créez un compte gratuit sur Cloudflare
2. Ajoutez votre domaine `ci-kiaba.com`
3. Changez les nameservers sur LWS vers ceux de Cloudflare
4. Configurez sur Cloudflare :
   - `@` → CNAME (proxied) vers `kiaba-rencontre-oqhr.onrender.com`
   - `www` → CNAME (proxied) vers `kiaba-rencontre-oqhr.onrender.com`
   - `@` → MX pour le mail (10 mail.ci-kiaba.com)

Cloudflare supporte CNAME flattening, donc vous pouvez avoir CNAME + MX sur @.

## 🔍 Vérification

Une fois configuré :
- `https://ci-kiaba.com` → doit pointer vers Render
- `https://www.ci-kiaba.com` → doit pointer vers Render
- Les deux doivent avoir le certificat SSL de Render

---

**Note** : Si vous gardez LWS pour le DNS, vous devrez peut-être contacter le support LWS pour savoir comment pointer vers Render tout en gardant le MX.

