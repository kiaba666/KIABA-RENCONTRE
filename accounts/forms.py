from django import forms
from .models import RechargePackage, BoostOption


class RechargeForm(forms.Form):
    """Formulaire pour choisir une formule de recharge"""
    package = forms.ModelChoiceField(
        queryset=RechargePackage.objects.filter(is_active=True),
        widget=forms.RadioSelect(attrs={"class": "space-y-2"}),
        label="Choisissez une formule",
        empty_label=None,
    )


class BoostForm(forms.Form):
    """Formulaire pour booster une annonce"""
    boost_option = forms.ModelChoiceField(
        queryset=BoostOption.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-lg"}),
        label="Type de boost",
        empty_label="-- Sélectionner --",
    )
    use_free_booster = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Utiliser un booster gratuit (si disponible)",
        help_text="Vous pouvez utiliser un booster gratuit au lieu de payer",
    )
