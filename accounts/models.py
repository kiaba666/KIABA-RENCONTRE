from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
import random


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        PROVIDER = "provider", _("Provider")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.PROVIDER,
        help_text=_("User role. Only providers can sign up publicly."),
    )
    phone_e164 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^\+[1-9]\d{1,14}$", message=_("Enter a valid E.164 phone."))],
        help_text=_("Phone number in E.164 format, e.g., +2250700000000"),
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=120)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio_sanitized = models.TextField(blank=True, default="")
    whatsapp_e164 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^\+[1-9]\d{1,14}$", message=_("Enter a valid E.164 phone."))],
    )
    telegram = models.CharField(max_length=64, null=True, blank=True)
    city = models.ForeignKey("ads.City", on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=2, default="CI")
    contact_prefs = models.JSONField(
        default=list,
        help_text=_("Subset of ['sms','whatsapp','call']"),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Profile verified by email"),
    )

    def __str__(self) -> str:  # pragma: no cover
        if hasattr(self, "user") and self.user:
            return f"Profile({self.user.username})"
        return f"Profile({self.display_name})"


def create_profile(sender, instance, created, **kwargs):  # pragma: no cover
    if created:
        Profile.objects.create(user=instance, display_name=instance.username)


models.signals.post_save.connect(create_profile, sender=CustomUser)

# Create your models here.


class EmailOTP(models.Model):
    class Purpose(models.TextChoices):
        PASSWORD_CHANGE = "password_change", _("Password change")
        LOGIN_DEVICE = "login_device", _("Login device notification")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_otps"
    )
    code = models.CharField(max_length=5)
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"OTP({self.user_id},{self.purpose},{self.code})"

    @staticmethod
    def generate_code() -> str:
        return f"{random.randint(0, 99999):05d}"

    @classmethod
    def create_otp(cls, user, purpose: str, ttl_seconds: int = 600) -> "EmailOTP":
        now = timezone.now()
        code = cls.generate_code()
        otp = cls.objects.create(
            user=user,
            code=code,
            purpose=purpose,
            expires_at=now + timezone.timedelta(seconds=ttl_seconds),
        )
        return otp

    def is_valid(self, code: str) -> bool:
        return not self.is_used and self.code == code and timezone.now() <= self.expires_at
