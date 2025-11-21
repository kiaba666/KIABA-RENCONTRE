from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_profile_validation_email(self, profile_id):
    """Envoyer un email de validation de profil"""
    try:
        profile = Profile.objects.get(id=profile_id)
        user = profile.user

        # Créer le lien de validation (à implémenter selon tes besoins)
        validation_url = f"{settings.SITE_URL}/accounts/validate-profile/{profile.id}/"

        subject = "Validation de votre profil KIABA"

        message = f"""
Bonjour {user.username},

Votre profil a été créé avec succès sur KIABA !

Pour finaliser votre inscription et commencer à publier des annonces, veuillez cliquer sur le lien ci-dessous pour valider votre profil :

{validation_url}

Informations de votre profil :
- Nom d'affichage : {profile.display_name}
- Ville : {profile.city}
- Méthodes de contact : {', '.join(profile.contact_prefs) if profile.contact_prefs else 'Non définies'}

Une fois validé, vous pourrez :
- Publier des annonces gratuitement
- Gérer vos préférences de contact
- Suivre les statistiques de vos annonces

Si vous n'avez pas créé de compte sur KIABA, veuillez ignorer cet email.

Cordialement,
L'équipe KIABA
{settings.DEFAULT_FROM_EMAIL}
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return f"Email de validation envoyé à {user.email}"

    except Profile.DoesNotExist:
        return f"Profil {profile_id} introuvable"
    except Exception as e:
        raise e


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_account_created_email(self, user_id):
    """Envoyer un email de confirmation de création de compte"""
    try:
        from .models import CustomUser

        user = CustomUser.objects.get(id=user_id)

        subject = "Compte créé avec succès sur KIABA"

        message = f"""
Bonjour {user.username},

Votre compte a été créé avec succès sur KIABA !

Prochaines étapes :
1. Vérifiez votre email pour confirmer votre compte
2. Complétez votre profil
3. Commencez à publier vos annonces

Si vous avez des questions, n'hésitez pas à nous contacter.

Cordialement,
L'équipe KIABA
{settings.DEFAULT_FROM_EMAIL}
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return f"Email de confirmation envoyé à {user.email}"

    except Exception as e:
        raise e


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_ad_published_email(self, ad_id):
    """Email de confirmation quand une annonce est publiée"""
    try:
        from ads.models import Ad

        ad = Ad.objects.get(id=ad_id)
        user = ad.user

        context = {
            "user": user,
            "ad": ad,
            "site_name": "KIABA",
            "site_url": settings.SITE_URL,
            "ad_url": f"{settings.SITE_URL}/ads/{ad.slug}/",
        }

        subject = f"[KIABA] Votre annonce '{ad.title}' est en ligne !"
        message = render_to_string("account/email/ad_published_message.txt", context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise e


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_login_notification_email(self, user_id):
    """Email de notification à chaque connexion"""
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.get(id=user_id)

        context = {
            "user": user,
            "site_name": "KIABA",
            "site_url": settings.SITE_URL,
        }

        subject = "[KIABA] Connexion détectée"
        message = render_to_string("account/email/login_notification_message.txt", context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise e


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_password_change_email(self, user_id):
    """Email de confirmation lors du changement de mot de passe"""
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.get(id=user_id)

        context = {
            "user": user,
            "site_name": "KIABA",
            "site_url": settings.SITE_URL,
        }

        subject = "[KIABA] Mot de passe modifié"
        message = render_to_string("account/email/password_change_message.txt", context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise e


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def send_ad_expiration_email(self, ad_id):
    """Email de notification quand une annonce expire"""
    try:
        from ads.models import Ad

        ad = Ad.objects.get(id=ad_id)
        user = ad.user

        context = {
            "user": user,
            "ad": ad,
            "site_name": "KIABA",
            "site_url": settings.SITE_URL,
            "ad_url": f"{settings.SITE_URL}/ads/{ad.slug}/",
        }

        subject = f"[KIABA] Votre annonce '{ad.title}' a expiré"
        message = render_to_string("account/email/ad_expiration_message.txt", context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise e
