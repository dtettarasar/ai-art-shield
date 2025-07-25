# protection_app/forms.py

from django import forms

class ImageUploadForm(forms.Form):
    # Champ pour l'upload de fichier.
    # Permet uniquement les fichiers image (validé par le navigateur et Django).
    image = forms.ImageField(
        label="Sélectionnez une image",
        help_text="Formats supportés : JPG, PNG, GIF, WEBP."
    )

    # Champ pour la force de protection (slider HTML).
    # min_value=0, max_value=1, step_size=0.01 pour un slider précis.
    strength = forms.DecimalField(
        label="Force de protection",
        min_value=0.0,
        max_value=30.0,
        initial=15.0, # Valeur par défaut
        max_digits=4, # Ex: 0.0 à 30.0
        decimal_places=2, # Deux chiffres après la virgule
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.10'}) # Pour le rendre un slider HTML
    )
