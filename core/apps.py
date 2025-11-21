from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """Configure le site Django après le chargement"""
        from django.contrib.sites.models import Site
        from django.conf import settings
        from django.db import connection

        def update_site_domain(sender, **kwargs):
            """Met à jour le domaine du site - appelé après les migrations"""
            try:
                # Vérifier que la base de données est accessible
                if not connection.ensure_connection():
                    return
                
                # Use get_or_create to avoid errors if Site doesn't exist
                site, created = Site.objects.get_or_create(
                    id=settings.SITE_ID,
                    defaults={
                        "domain": "ci-kiaba.com",
                        "name": "KIABA",
                    }
                )
                # Update if it already exists and domain is different
                if not created and site.domain != "ci-kiaba.com":
                    site.domain = "ci-kiaba.com"
                    site.name = "KIABA"
                    site.save()
            except Exception:
                # Silently fail to prevent startup errors
                pass

        # Ne pas appeler immédiatement - seulement après migrations
        # Cela évite d'accéder à la base de données pendant l'initialisation
        post_migrate.connect(update_site_domain, sender=self)
