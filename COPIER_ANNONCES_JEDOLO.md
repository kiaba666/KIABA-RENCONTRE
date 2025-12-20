# Instructions : Copier les Vraies Annonces depuis ci.jedolo.com

## 🎯 Ce que vous devez faire

Copier **EXACTEMENT** les annonces depuis ci.jedolo.com dans le fichier `jedolo_ads_data.py`

## 📋 Étapes Détaillées

### 1. Ouvrir le Fichier

Ouvrez : `core/management/commands/jedolo_ads_data.py`

### 2. Aller sur ci.jedolo.com

1. Ouvrez https://ci.jedolo.com dans votre navigateur
2. Parcourez les annonces
3. Cliquez sur chaque annonce pour voir les détails complets

### 3. Pour Chaque Annonce, Copiez :

#### a) Le Titre
- Copiez le titre **EXACTEMENT** tel qu'il apparaît sur le site
- Exemple : "Belle jeune femme disponible Abidjan Cocody"

#### b) La Description
- Copiez la description **COMPLÈTE** et **EXACTE**
- Ne modifiez rien, copiez mot pour mot

#### c) Le Numéro de Téléphone
- Copiez le numéro **EXACT**
- Convertissez-le en format E.164 : `+225XXXXXXXXXX`
- Exemple : Si vous voyez "07 12 34 56 78" → `+2250712345678`
- Exemple : Si vous voyez "+225 07 12 34 56 78" → `+2250712345678` (enlever les espaces)

#### d) La Catégorie
- `"rencontres_escort"` pour Rencontres et escortes
- `"massages_services"` pour Massages et services
- `"produits_adultes"` pour Produits adultes

#### e) Les Sous-catégories
- Exemples : `["Escort Girls"]`, `["Massage Relaxant"]`, `["Cherche Homme"]`, etc.

### 4. Format dans le Fichier

Ajoutez chaque annonce dans ce format **EXACT** :

```python
{
    "title": "TITRE EXACT depuis le site",
    "description": "DESCRIPTION EXACTE depuis le site - copiez mot pour mot",
    "category": "rencontres_escort",
    "subcategories": ["Escort Girls"],
    "phone": "+2250712345678",
},
```

## 📝 Exemple Concret

Si sur ci.jedolo.com vous voyez :

```
Titre: Belle jeune femme disponible Abidjan Cocody
Description: Jeune femme élégante disponible 24/7. Service de qualité. 
Appelez-moi pour plus d'informations. Discrétion garantie.
Numéro: 07 12 34 56 78
```

Dans le fichier, écrivez :

```python
{
    "title": "Belle jeune femme disponible Abidjan Cocody",
    "description": "Jeune femme élégante disponible 24/7. Service de qualité. Appelez-moi pour plus d'informations. Discrétion garantie.",
    "category": "rencontres_escort",
    "subcategories": ["Escort Girls"],
    "phone": "+2250712345678",
},
```

## 🔢 Conversion des Numéros

| Format sur le site | Format dans le fichier |
|---------------------|------------------------|
| `07 12 34 56 78` | `+2250712345678` |
| `+225 07 12 34 56 78` | `+2250712345678` |
| `225 07 12 34 56 78` | `+2250712345678` |
| `+2250712345678` | `+2250712345678` (déjà bon) |

**Règle** : Toujours commencer par `+225` et enlever tous les espaces

## 📊 Combien d'Annonces ?

Pour créer 300 annonces :
- **Minimum** : 30 annonces différentes (réutilisées 10 fois)
- **Recommandé** : 50-100 annonces différentes (plus de variété)

## ✅ Checklist

Pour chaque annonce copiée, vérifiez :

- [ ] Titre copié EXACTEMENT
- [ ] Description copiée EXACTEMENT (mot pour mot)
- [ ] Numéro en format E.164 (`+225XXXXXXXXXX`)
- [ ] Catégorie correcte
- [ ] Sous-catégories correctes
- [ ] Virgule à la fin (sauf la dernière)

## 🚀 Après Avoir Rempli

1. Sauvegardez le fichier `jedolo_ads_data.py`
2. Commitez et poussez :
   ```bash
   git add core/management/commands/jedolo_ads_data.py
   git commit -m "Add: Vraies annonces depuis ci.jedolo.com"
   git push origin master
   ```
3. Exécutez le script sur Render :
   ```bash
   python manage.py import_from_jedolo --users 100 --ads 300
   ```

## ⚠️ IMPORTANT

- **NE MODIFIEZ RIEN** - copiez exactement
- Les numéros doivent être **EXACTS** comme sur le site
- Les descriptions doivent être **COMPLÈTES** et **EXACTES**
- Les titres doivent être **EXACTS**

---

**Le fichier à modifier** : `core/management/commands/jedolo_ads_data.py`

