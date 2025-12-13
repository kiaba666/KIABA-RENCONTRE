# Changer de compte GitHub dans le terminal

## Étape 1 : Supprimer les credentials GitHub stockés

### Option A : Supprimer via Keychain Access (macOS)

1. Ouvrez **Keychain Access** (Accès au trousseau) sur votre Mac
2. Recherchez **"github.com"**
3. Supprimez toutes les entrées liées à GitHub
4. Ou supprimez via le terminal :

```bash
# Supprimer les credentials GitHub du keychain
git credential-osxkeychain erase
host=github.com
protocol=https
# (Appuyez deux fois sur Entrée)
```

### Option B : Supprimer via la ligne de commande

```bash
# Supprimer les credentials pour github.com
printf "host=github.com\nprotocol=https\n" | git credential-osxkeychain erase
```

## Étape 2 : Vérifier la configuration Git locale

```bash
cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-master

# Vérifier le nom d'utilisateur configuré
git config user.name

# Vérifier l'email configuré
git config user.email

# Si ce n'est pas kiaba666, configurez-le :
git config user.name "kiaba666"
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

## Étape 4 : Faire le push (vous serez demandé de vous authentifier)

```bash
git push -u origin main
```

Quand Git vous demande :
- **Username** : `kiaba666`
- **Password** : Votre **Personal Access Token** du compte kiaba666

## Si vous n'avez pas de token pour kiaba666

1. Connectez-vous sur GitHub avec le compte **kiaba666**
2. Allez sur : https://github.com/settings/tokens
3. Cliquez sur **"Generate new token"** → **"Generate new token (classic)"**
4. Donnez un nom (ex: "KIABA-RENCONTRE")
5. Cochez la permission **"repo"** (toutes les sous-permissions)
6. Cliquez sur **"Generate token"**
7. **COPIEZ LE TOKEN**

## Commandes complètes à exécuter

```bash
# 1. Aller dans le répertoire
cd /Users/mac.chaka/Desktop/KIABA-RENCONTRE-master

# 2. Supprimer les anciens credentials
printf "host=github.com\nprotocol=https\n" | git credential-osxkeychain erase

# 3. Configurer le bon compte
git config user.name "kiaba666"
git config user.email "VOTRE_EMAIL_KIABA666@example.com"

# 4. Vérifier le remote
git remote -v

# 5. Faire le push (vous serez demandé username + token)
git push -u origin main
```

