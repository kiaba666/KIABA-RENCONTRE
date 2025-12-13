# Commandes pour se connecter au compte GitHub kiaba666

## 1. Configurer Git avec le compte kiaba666

```bash
# Configurer le nom d'utilisateur (remplacez par l'email associé à kiaba666)
git config user.name "kiaba666"
git config user.email "VOTRE_EMAIL_KIABA666@example.com"
```

## 2. Vérifier la configuration

```bash
git config user.name
git config user.email
```

## 3. Options pour l'authentification GitHub

### Option A : Utiliser un Personal Access Token (Recommandé)

1. Créer un token sur GitHub :
   - Allez sur https://github.com/settings/tokens
   - Cliquez sur "Generate new token (classic)"
   - Donnez-lui les permissions "repo"
   - Copiez le token

2. Utiliser le token lors du push :
```bash
git push -u origin main
# Quand demandé :
# Username: kiaba666
# Password: [collez votre token ici]
```

### Option B : Configurer Git Credential Helper (macOS)

```bash
# Configurer le credential helper pour macOS
git config --global credential.helper osxkeychain

# Ensuite lors du push, entrez vos identifiants une fois
git push -u origin main
```

### Option C : Utiliser SSH (Plus sécurisé)

```bash
# 1. Générer une clé SSH (si vous n'en avez pas)
ssh-keygen -t ed25519 -C "VOTRE_EMAIL_KIABA666@example.com"

# 2. Copier la clé publique
cat ~/.ssh/id_ed25519.pub

# 3. Ajouter la clé sur GitHub :
# - Allez sur https://github.com/settings/keys
# - Cliquez sur "New SSH key"
# - Collez la clé publique

# 4. Changer l'URL du remote pour utiliser SSH
git remote set-url origin git@github.com:kiaba666/KIABA-RENCONTRE.git

# 5. Tester la connexion
ssh -T git@github.com

# 6. Push
git push -u origin main
```

## 4. Vérifier le remote

```bash
git remote -v
```

Si l'URL n'est pas correcte :
```bash
git remote set-url origin https://github.com/kiaba666/KIABA-RENCONTRE.git
```

## 5. Faire le push

```bash
git push -u origin main
```

