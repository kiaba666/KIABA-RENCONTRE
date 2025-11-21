from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from allauth.account.forms import SignupForm, LoginForm
from .models import Profile, EmailOTP
from .widgets import (
    StyledTextInput,
    StyledEmailInput,
    StyledPasswordInput,
    StyledCurrentPasswordInput,
)


class JSONMultipleChoiceField(forms.MultipleChoiceField):
    """Champ personnalisé pour gérer les JSONField avec MultipleChoiceField"""

    def prepare_value(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            import json

            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return [value]


class ProfileEditForm(forms.ModelForm):
    """Formulaire pour modifier le profil utilisateur"""

    phone_e164 = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "+225XXXXXXXXX",
            }
        ),
        label="Numéro de téléphone",
        help_text="Numéro principal pour les appels et SMS",
    )

    contact_prefs = JSONMultipleChoiceField(
        choices=[
            ("sms", "SMS"),
            ("whatsapp", "WhatsApp"),
            ("call", "Appel téléphonique"),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        required=False,
        label="Méthodes de contact",
        help_text="Sélectionnez les moyens par lesquels les clients peuvent vous contacter",
    )

    class Meta:
        model = Profile
        fields = [
            "display_name",
            "whatsapp_e164",
            "bio_sanitized",
            "city",
        ]
        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            "whatsapp_e164": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                    "placeholder": "+225XXXXXXXXX",
                }
            ),
            "bio_sanitized": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                    "rows": 4,
                    "placeholder": "Décrivez-vous brièvement...",
                }
            ),
            "city": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                }
            ),
        }
        labels = {
            "display_name": "Nom d'affichage",
            "whatsapp_e164": "Numéro WhatsApp",
            "bio_sanitized": "Biographie",
            "city": "Ville",
        }
        help_texts = {
            "display_name": "Le nom qui apparaîtra sur vos annonces",
            "whatsapp_e164": "Numéro WhatsApp (peut être différent du téléphone)",
            "bio_sanitized": "Description courte de vos services",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplir les valeurs existantes pour contact_prefs
        if self.instance and self.instance.pk and self.instance.contact_prefs:
            self.fields["contact_prefs"].initial = self.instance.contact_prefs


class CustomLoginForm(LoginForm):
    """Formulaire de connexion personnalisé avec style"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Styliser les champs avec les bons attributs autocomplete
        self.fields["login"].widget = StyledEmailInput()
        self.fields["password"].widget = StyledCurrentPasswordInput()


class CustomSignupForm(SignupForm):
    """Formulaire d'inscription personnalisé avec style"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Styliser les champs avec les bons attributs autocomplete
        self.fields["username"].widget = StyledTextInput(attrs={"autocomplete": "username"})
        self.fields["email"].widget = StyledEmailInput()
        self.fields["password1"].widget = StyledPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
        self.fields["password2"].widget = StyledPasswordInput(
            attrs={"autocomplete": "new-password"}
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulaire personnalisé pour changer le mot de passe"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Styliser les champs avec les bons attributs autocomplete
        self.fields["old_password"].widget = StyledCurrentPasswordInput()
        self.fields["new_password1"].widget = StyledPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
        self.fields["new_password2"].widget = StyledPasswordInput(
            attrs={"autocomplete": "new-password"}
        )

        # Libellés exacts
        self.fields["old_password"].label = "Ancien mot de passe"
        self.fields["new_password1"].label = "Nouveau mot de passe"
        self.fields["new_password2"].label = "Confirmation du nouveau mot de passe"

        # Aide exacte pour le nouveau mot de passe (affichée telle quelle dans le template)
        self.fields["new_password1"].help_text = (
            "Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.<br>"
            "Votre mot de passe doit contenir au minimum 8 caractères.<br>"
            "Votre mot de passe ne peut pas être un mot de passe couramment utilisé.<br>"
            "Votre mot de passe ne peut pas être entièrement numérique."
        )

        # Pas d'aide pour les autres champs
        self.fields["old_password"].help_text = ""
        self.fields["new_password2"].help_text = (
            "Saisissez le même mot de passe que précédemment, pour vérification."
        )


class PasswordChangeOTPRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self) -> EmailOTP:
        otp = EmailOTP.create_otp(self.user, EmailOTP.Purpose.PASSWORD_CHANGE)
        return otp


class PasswordChangeWithOTPForm(CustomPasswordChangeForm):
    code = forms.CharField(max_length=5, label="Code reçu par email")

    def clean(self):
        cleaned = super().clean()
        code = cleaned.get("code")
        if not code or len(code) != 5:
            raise forms.ValidationError("Code OTP invalide")
        otp = (
            EmailOTP.objects.filter(
                user=self.user,
                purpose=EmailOTP.Purpose.PASSWORD_CHANGE,
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )
        if not otp or not otp.is_valid(code):
            raise forms.ValidationError("Code OTP incorrect ou expiré")
        self._otp_obj = otp
        return cleaned

    def save(self, commit=True):
        user = super().save(commit)
        if hasattr(self, "_otp_obj"):
            self._otp_obj.is_used = True
            self._otp_obj.save(update_fields=["is_used"])
        return user
