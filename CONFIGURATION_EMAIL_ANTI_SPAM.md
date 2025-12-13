# Configuration Email Anti-Spam pour KIABA

## Problème : Les emails vont dans les spams

Pour éviter que les emails KIABA soient marqués comme spam, il faut configurer correctement les enregistrements DNS.

## Configuration DNS requise

### 1. SPF (Sender Policy Framework)

Ajoutez cet enregistrement TXT dans votre DNS pour le domaine `ci-kiaba.com` :

```
v=spf1 include:mail55.lwspanel.com ~all
```

Ou si vous utilisez plusieurs serveurs :

```
v=spf1 include:mail55.lwspanel.com ip4:VOTRE_IP_SERVEUR ~all
```

### 2. DKIM (DomainKeys Identified Mail)

Contactez votre hébergeur email (lwspanel.com) pour obtenir :
- La clé publique DKIM
- Le sélecteur DKIM (généralement "default" ou "mail")

Ajoutez ensuite l'enregistrement TXT dans votre DNS :

```
default._domainkey.ci-kiaba.com TXT "v=DKIM1; k=rsa; p=VOTRE_CLE_PUBLIQUE_DKIM"
```

### 3. DMARC (Domain-based Message Authentication)

Ajoutez cet enregistrement TXT dans votre DNS :

```
_dmarc.ci-kiaba.com TXT "v=DMARC1; p=quarantine; rua=mailto:support@ci-kiaba.com; ruf=mailto:support@ci-kiaba.com; sp=quarantine; aspf=r;"
```

### 4. Reverse DNS (PTR)

Assurez-vous que votre serveur email a un enregistrement PTR correct pointant vers `ci-kiaba.com`.

## Vérification

Utilisez ces outils pour vérifier votre configuration :

1. **SPF Checker** : https://mxtoolbox.com/spf.aspx
2. **DKIM Checker** : https://mxtoolbox.com/dkim.aspx
3. **DMARC Checker** : https://mxtoolbox.com/dmarc.aspx
4. **Email Deliverability Test** : https://www.mail-tester.com/

## Configuration dans le code

Le code Django est déjà configuré avec :
- Headers personnalisés pour améliorer la réputation
- Format d'email standardisé avec nom "KIABA"
- Templates HTML/text professionnels
- Gestion d'erreurs et retry automatique

## Contact avec l'hébergeur email

Contactez **lwspanel.com** pour :
1. Obtenir les informations DKIM
2. Vérifier que le serveur email est correctement configuré
3. Demander l'ajout de votre domaine dans leur whitelist

## Notes importantes

- Les changements DNS peuvent prendre jusqu'à 48h pour se propager
- Testez toujours vos emails avec mail-tester.com avant de les envoyer en masse
- Surveillez les taux de délivrabilité et ajustez si nécessaire

