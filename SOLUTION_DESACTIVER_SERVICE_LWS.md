# Solution : Désactiver le Service Web LWS pour ci-kiaba.com

## 🔴 Problème Identifié

Le domaine `ci-kiaba.com` affiche la page par défaut de LWS au lieu de votre site Django sur Render.

**Cause** : Un service web LWS est activé pour ce domaine et intercepte les requêtes avant qu'elles n'atteignent Render.

## ✅ Solution : Désactiver le Service Web LWS

### Étapes sur LWS Panel

1. **Connectez-vous à LWS Panel** : https://www.lwspanel.com

2. **Allez dans la gestion du domaine** `ci-kiaba.com`

3. **Cherchez la section "Hébergement Web" ou "Service Web"**

4. **Désactivez le service web** pour ce domaine :
   - Cherchez un bouton "Désactiver" ou "Supprimer"
   - Ou une option "Aucun service web" / "Pas d'hébergement"
   - Ou "Désactiver l'hébergement"

5. **Sauvegardez les modifications**

### Alternative : Vérifier la Configuration DNS

Si vous ne trouvez pas l'option pour désactiver le service web :

1. **Allez dans la section DNS** du domaine
2. **Vérifiez l'enregistrement A pour @** :
   - Doit pointer vers `216.24.57.7` (Render)
   - **NE DOIT PAS** pointer vers `91.216.107.201` (LWS)

3. **Si l'enregistrement A pointe vers LWS** :
   - Modifiez-le pour pointer vers `216.24.57.7`
   - Sauvegardez

### Vérification après Modification

Après avoir désactivé le service web LWS :

1. **Attendez 5-10 minutes** pour que les changements prennent effet
2. **Testez** : `https://ci-kiaba.com`
3. **Vous devriez voir** : La page d'âge (18+) puis votre site Django

## 📋 Checklist

- [ ] Service web LWS désactivé pour `ci-kiaba.com`
- [ ] Enregistrement A pour `@` = `216.24.57.7` (pas `91.216.107.201`)
- [ ] Attendu 5-10 minutes
- [ ] Testé `https://ci-kiaba.com`
- [ ] Site Django visible

## 🔍 Comment Vérifier si le Service Web est Activé

Sur LWS Panel, cherchez :
- Section "Hébergement Web"
- Section "Service Web"
- Section "Hébergement"
- Indicateur "Service activé" ou "Hébergement actif"

Si vous voyez un de ces éléments, le service web est activé et doit être désactivé.

## 💡 Note Importante

**Le DNS pointe bien vers Render** (`216.24.57.7`), mais LWS intercepte les requêtes HTTP/HTTPS avant qu'elles n'atteignent Render car un service web est activé.

Une fois le service web désactivé, les requêtes passeront directement à Render et vous verrez votre site Django.

---

**Si vous ne trouvez pas l'option pour désactiver le service web**, contactez le support LWS et demandez-leur de désactiver le service web pour `ci-kiaba.com` car vous utilisez un hébergement externe (Render).

