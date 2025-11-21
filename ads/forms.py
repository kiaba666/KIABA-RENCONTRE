from django import forms
from django.core.exceptions import ValidationError
import bleach
from .models import Ad, City


class AdForm(forms.Form):
    """Formulaire unique pour créer une annonce"""

    title = forms.CharField(
        max_length=140,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Titre de votre annonce",
            }
        ),
        label="Titre de l'annonce",
    )

    category = forms.ChoiceField(
        choices=Ad.Category.choices,
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            }
        ),
        label="Catégorie",
    )

    subcategories = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        required=False,
        label="Sous-catégories",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mettre à jour les sous-catégories selon la catégorie sélectionnée
        if "data" in kwargs:
            category = kwargs["data"].get("category")
            if category:
                self.fields["subcategories"].choices = self.get_subcategory_choices(category)
        elif "initial" in kwargs and "category" in kwargs["initial"]:
            category = kwargs["initial"]["category"]
            self.fields["subcategories"].choices = self.get_subcategory_choices(category)

        # Toujours initialiser avec toutes les sous-catégories possibles pour éviter les erreurs de validation
        if not self.fields["subcategories"].choices:
            all_subcategories = []
            for category_choices in (
                self.get_subcategory_choices("rencontres_escort")
                + self.get_subcategory_choices("massages_services")
                + self.get_subcategory_choices("produits_adultes")
            ):
                all_subcategories.append(category_choices)
            self.fields["subcategories"].choices = all_subcategories

    def get_subcategory_choices(self, category):
        """Retourne les sous-catégories selon la catégorie"""
        subcategory_mapping = {
            "rencontres_escort": [
                "sodomie",
                "Cherche Homme",
                "Cherche Femme",
                "vaginal",
                "Escort Girls",
                "Escort Boys",
                "fellation",
            ],
            "massages_services": [
                "vaginal",
                "fellation",
                "Massage sensuel ou érotique",
                "Massage Ivoirien",
                "Massage Relaxant",
                "Massage sportif",
                "Massage chinois",
                "Massage Intégral",
                "sodomie",
            ],
            "produits_adultes": [
                "Aphrodisiaques homme",
                "Sextoy - Jouet Sexuel",
                "Lubrifiants – Huiles",
                "Aphrodisiaques Femme",
                "Parfums adultes",
            ],
        }
        subcategories = subcategory_mapping.get(category, [])
        return [(choice, choice) for choice in subcategories]

    def clean_subcategories(self):
        # Convertir la liste en JSON pour le stockage
        subcategories = self.cleaned_data.get("subcategories", [])
        return subcategories

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "rows": 5,
                "placeholder": "Description détaillée de votre annonce...",
            }
        ),
        label="Description",
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            }
        ),
        label="Ville",
    )

    phone1 = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "+225XXXXXXXXX",
            }
        ),
        label="Numéro de téléphone 1",
        help_text="Numéro principal pour les appels et SMS",
    )

    phone2 = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "+225XXXXXXXXX (optionnel)",
            }
        ),
        label="Numéro de téléphone 2 (optionnel)",
    )

    contact_methods = forms.MultipleChoiceField(
        choices=[
            ("sms", "SMS"),
            ("whatsapp", "WhatsApp"),
            ("call", "Appel téléphonique"),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        required=True,
        label="Méthodes de contact",
        help_text="Sélectionnez les moyens par lesquels les clients peuvent vous contacter",
    )

    image1 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "accept": "image/*",
            }
        ),
        label="Photo 1",
    )

    image2 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "accept": "image/*",
            }
        ),
        label="Photo 2",
    )

    image3 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "accept": "image/*",
            }
        ),
        label="Photo 3",
    )

    image4 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "accept": "image/*",
            }
        ),
        label="Photo 4",
    )

    image5 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "accept": "image/*",
            }
        ),
        label="Photo 5",
    )

    def clean_description(self):
        description = self.cleaned_data["description"]
        # Sanitize HTML avec bleach
        sanitized = bleach.clean(description, tags=[], attributes={}, strip=True)
        return sanitized

    def clean(self):
        cleaned_data = super().clean()
        phone1 = cleaned_data.get("phone1")
        phone2 = cleaned_data.get("phone2")
        contact_methods = cleaned_data.get("contact_methods")

        if not phone1 and not phone2:
            raise ValidationError("Au moins un numéro de téléphone est requis.")

        if contact_methods and not (phone1 or phone2):
            self.add_error(
                "contact_methods",
                "Vous devez fournir un numéro de téléphone pour les méthodes de contact sélectionnées.",
            )

        return cleaned_data
