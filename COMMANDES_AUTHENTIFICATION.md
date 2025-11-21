# Commandes pour l'authentification GitHub - Compte kiaba666

## Étape 1 : Configurer le credential helper (pour stocker les identifiants)

```bash
cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-master
git config --global credential.helper osxkeychain
```

## Étape 2 : Vérifier la configuration Git

```bash
git config user.name
git config user.email
```

Si l'email n'est pas celui du compte kiaba666, configurez-le :
```bash
git config user.email "VOTRE_EMAIL_KIABA666@example.com"
```

## Étape 3 : Vérifier le remote

```bash
git remote -v
```

Doit afficher :
```
origin	https://github.com/kiaba666/KIABA-RENCONTRE.git (fetch)
origin	https://github.com/kiaba666/KIABA-RENCONTRE.git (push)
```

## Étape 4 : Créer un Personal Access Token sur GitHub

1. Allez sur : https://github.com/settings/tokens
2. Cliquez sur "Generate new token" → "Generate new token (classic)"
3. Donnez un nom au token (ex: "KIABA-RENCONTRE")
4. Sélectionnez les permissions : **repo** (cochez toutes les sous-permissions)
5. Cliquez sur "Generate token"
6. **COPIEZ LE TOKEN IMMÉDIATEMENT** (vous ne pourrez plus le voir après)

## Étape 5 : Faire le push (authentification)

```bash
cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-master
git push -u origin main
```

Quand Git vous demande :
- **Username** : `kiaba666`
- **Password** : Collez votre **Personal Access Token** (pas votre mot de passe GitHub)

## Alternative : Utiliser le token directement dans l'URL (moins sécurisé)

Si vous préférez, vous pouvez aussi utiliser le token directement :

```bash
git remote set-url origin https://kiaba666:VOTRE_TOKEN@github.com/kiaba666/KIABA-RENCONTRE.git
git push -u origin main
```

(Remplacez `VOTRE_TOKEN` par votre token)

## Vérification

Après le push réussi, vérifiez sur GitHub :
https://github.com/kiaba666/KIABA-RENCONTRE

---

## Résumé des commandes essentielles

```bash
# 1. Configurer credential helper
git config --global credential.helper osxkeychain

# 2. Configurer l'email (si nécessaire)
git config user.email "VOTRE_EMAIL_KIABA666@example.com"

# 3. Vérifier le remote
git remote -v

# 4. Faire le push (vous serez demandé username + token)
git push -u origin main
```

