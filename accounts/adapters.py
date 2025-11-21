from allauth.account.adapter import DefaultAccountAdapter


class NoRateLimitAccountAdapter(DefaultAccountAdapter):
    """Adaptateur personnalisé pour désactiver le rate limiting d'allauth"""

    def is_ajax(self, request):
        """Désactiver la vérification AJAX pour éviter les erreurs"""
        return False

    def get_login_redirect_url(self, request):
        """Redirection après connexion"""
        # Marquer le profil comme vérifié après la première connexion
        try:
            profile = request.user.profile
            if not profile.is_verified:
                profile.is_verified = True
                profile.save()
                print(f"Profil de {request.user.username} marqué comme vérifié")
        except Exception:
            pass

        # Envoyer l'email de notification de connexion
        from .tasks import send_login_notification_email

        send_login_notification_email.delay(request.user.id)
        return "/dashboard/"

    def get_logout_redirect_url(self, request):
        """Redirection après déconnexion"""
        return "/"

    def is_auto_signup_allowed(self, request, sociallogin):
        """Autoriser l'inscription automatique"""
        return True

    def is_open_for_signup(self, request):
        """Site ouvert aux inscriptions"""
        return True
