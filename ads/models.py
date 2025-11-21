from django.db import models, transaction
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    region = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Ville")
        verbose_name_plural = _("Villes")

    def save(self, *args, **kwargs):  # pragma: no cover
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Ad(models.Model):
    class Category(models.TextChoices):
        RENCONTRES_ESCORTES = "rencontres_escort", "Rencontres et escortes"
        MASSAGES_SERVICES = "massages_services", "Massages et services"
        PRODUITS_ADULTES = "produits_adultes", "Produits adultes"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        ARCHIVED = "archived", "Archived"

    SUBCATEGORY_CHOICES = [
        # Rencontres et escortes
        "sodomie",
        "Cherche Homme",
        "Cherche Femme",
        "vaginal",
        "Escort Girls",
        "Escort Boys",
        "fellation",
        # Massages et services
        "Massage sensuel ou érotique",
        "Massage Ivoirien",
        "Massage Relaxant",
        "Massage sportif",
        "Massage chinois",
        "Massage Intégral",
        # Produits adultes
        "Aphrodisiaques homme",
        "Sextoy - Jouet Sexuel",
        "Lubrifiants – Huiles",
        "Aphrodisiaques Femme",
        "Parfums adultes",
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description_sanitized = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    subcategories = models.JSONField(default=list)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    area = models.CharField(max_length=120, blank=True, default="")
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(max_length=180, unique=True)
    views_count = models.PositiveIntegerField(default=0)
    contacts_clicks = models.JSONField(default=dict)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    features = models.ManyToManyField(Feature, through="AdFeature", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        invalid = [s for s in self.subcategories if s not in self.SUBCATEGORY_CHOICES]
        if invalid:
            raise ValidationError({"subcategories": f"Invalid subcategories: {invalid}"})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:150]
            candidate = base
            idx = 1
            while Ad.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                idx += 1
                candidate = f"{base}-{idx}"
            self.slug = candidate
        # Initialize contacts_clicks structure
        if not self.contacts_clicks:
            self.contacts_clicks = {"sms": 0, "whatsapp": 0, "call": 0}
        # Set default expiration to 14 days if not set
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title

    def get_subcategories_display(self):
        """Retourne les sous-catégories sous forme de chaîne lisible"""
        if not self.subcategories:
            return "Aucune"
        return ", ".join(self.subcategories)

    get_subcategories_display.short_description = "Sous-catégories"


class AdMedia(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to="ads/")
    is_primary = models.BooleanField(default=False)

    def clean(self):
        # Enforce max 5 media per Ad
        existing = (
            AdMedia.objects.filter(ad=self.ad).exclude(pk=self.pk).count() if self.ad_id else 0
        )
        if existing >= 5:
            raise ValidationError("Maximum 5 photos per ad.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)
            # Ensure only one primary
            if self.is_primary:
                AdMedia.objects.filter(ad=self.ad).exclude(pk=self.pk).update(is_primary=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"Media({self.ad_id})"


class Availability(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name="availability")
    days_of_week = models.JSONField(default=list)
    time_ranges = models.JSONField(default=list)  # e.g., [{"start":"09:00","end":"18:00"}]
    on_request = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"Availability({self.ad_id})"


class AdFeature(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("ad", "feature")


class Report(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    reporter_fingerprint = models.CharField(max_length=128)
    reason = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)


# Create your models here.
