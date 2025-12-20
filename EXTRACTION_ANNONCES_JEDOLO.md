# Guide : Extraire les Vraies Annonces depuis ci.jedolo.com

## 🎯 Objectif

Copier **EXACTEMENT** les annonces depuis ci.jedolo.com avec :
- ✅ Mêmes titres
- ✅ Mêmes descriptions
- ✅ Mêmes numéros de téléphone
- ✅ **AUCUNE modification**

## 📋 Méthode : Copie Manuelle

### Étape 1 : Aller sur ci.jedolo.com

1. Ouvrez https://ci.jedolo.com dans votre navigateur
2. Parcourez les annonces
3. Cliquez sur chaque annonce pour voir les détails

### Étape 2 : Copier les Informations

Pour chaque annonce, copiez **EXACTEMENT** :

1. **Titre** : Copiez le titre tel quel
2. **Description** : Copiez la description complète
3. **Numéro de téléphone** : Copiez le numéro exact (format: +225XXXXXXXXXX)
4. **Catégorie** : Déterminez la catégorie (rencontres_escort, massages_services, produits_adultes)
5. **Sous-catégories** : Notez les sous-catégories

### Étape 3 : Ajouter dans jedolo_ads_data.py

Ouvrez le fichier `core/management/commands/jedolo_ads_data.py` et ajoutez chaque annonce dans ce format :

```python
{
    "title": "TITRE EXACT depuis le site",
    "description": "DESCRIPTION EXACTE depuis le site",
    "category": "rencontres_escort",  # ou "massages_services" ou "produits_adultes"
    "subcategories": ["Escort Girls"],  # ou autres
    "phone": "+225XXXXXXXXXX",  # NUMÉRO EXACT
},
```

## 📝 Exemple

Si sur ci.jedolo.com vous voyez :

**Titre** : "Belle jeune femme disponible Abidjan Cocody"
**Description** : "Jeune femme élégante disponible 24/7. Service de qualité. Appelez-moi."
**Numéro** : "+225 07 12 34 56 78"

Dans le fichier, écrivez **EXACTEMENT** :

```python
{
    "title": "Belle jeune femme disponible Abidjan Cocody",
    "description": "Jeune femme élégante disponible 24/7. Service de qualité. Appelez-moi.",
    "category": "rencontres_escort",
    "subcategories": ["Escort Girls"],
    "phone": "+2250712345678",  # Convertir en format E.164 (sans espaces)
},
```

## 🔢 Format des Numéros

Les numéros doivent être en format E.164 :
- ✅ `+2250712345678` (correct)
- ❌ `+225 07 12 34 56 78` (espaces à enlever)
- ❌ `07 12 34 56 78` (ajouter +225)
- ❌ `2250712345678` (ajouter le +)

## 📊 Nombre d'Annonces

Pour créer 300 annonces, vous avez besoin d'au moins **30-50 annonces différentes** (elles seront réutilisées).

## ✅ Vérification

Après avoir ajouté les annonces :

1. Vérifiez que les titres sont EXACTS
2. Vérifiez que les descriptions sont EXACTES
3. Vérifiez que les numéros sont EXACTS
4. Vérifiez le format E.164 pour les numéros

## 🚀 Utilisation

Une fois les vraies annonces ajoutées dans `jedolo_ads_data.py` :

```bash
python manage.py import_from_jedolo --users 100 --ads 300
```

Le script utilisera ces annonces EXACTES avec leurs numéros.

---

**IMPORTANT** : Copiez EXACTEMENT sans modifier. Les numéros doivent être les mêmes que sur ci.jedolo.com.

