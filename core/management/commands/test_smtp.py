"""
Commande pour tester l'envoi d'email SMTP en production
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.email_service import EmailService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Test SMTP email sending"

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            type=str,
            required=True,
            help="Email address to send test to",
        )

    def handle(self, *args, **options):
        to_email = options["to"]

        self.stdout.write("=" * 60)
        self.stdout.write("TEST D'ENVOI D'EMAIL SMTP")
        self.stdout.write("=" * 60)
        
        self.stdout.write(f"\n📧 Configuration actuelle:")
        self.stdout.write(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        self.stdout.write(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Non défini'}")
        self.stdout.write(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"  DEBUG: {settings.DEBUG}")
        
        self.stdout.write(f"\n📤 Tentative d'envoi d'email à: {to_email}")
        
        try:
            success = EmailService.send_email(
                subject="Test Email SMTP - KIABA",
                to_emails=[to_email],
                text_content="""Bonjour,

Ceci est un email de test pour vérifier la configuration SMTP de KIABA.

Si vous recevez cet email, la configuration SMTP fonctionne correctement.

Cordialement,
L'équipe KIABA""",
                html_content="""<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #3b82f6;">Test Email SMTP - KIABA</h2>
    <p>Bonjour,</p>
    <p>Ceci est un email de test pour vérifier la configuration SMTP de KIABA.</p>
    <p>Si vous recevez cet email, la configuration SMTP fonctionne correctement.</p>
    <p>Cordialement,<br><strong>L'équipe KIABA</strong></p>
</body>
</html>""",
                fail_silently=False,
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"\n✅ Email envoyé avec succès à {to_email}"))
                self.stdout.write("Vérifiez votre boîte mail (et les spams) pour confirmer la réception.")
            else:
                self.stdout.write(self.style.ERROR(f"\n❌ Échec de l'envoi d'email à {to_email}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Erreur lors de l'envoi: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())

