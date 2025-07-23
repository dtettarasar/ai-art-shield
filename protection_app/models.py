from django.db import models
from django.conf import settings
import datetime

class ProtectedImage(models.Model):
    # Un identifiant unique (UUID) pour le fichier, qui est aussi la clé primaire de la ligne.
    uuid = models.UUIDField(primary_key=True, editable=False)

    # Le nom du fichier image original (pour l'affichage à l'utilisateur)
    original_filename = models.CharField(max_length=255)

    # Le chemin relatif vers le fichier image protégé
    protected_image_path = models.CharField(max_length=255)

    # Le chemin relatif vers le fichier original (optionnel)
    original_image_path = models.CharField(max_length=255)

    # La force de protection appliquée (DecimalField pour plus de précision)
    protection_strength = models.DecimalField(max_digits=3, decimal_places=2)

    # Date et heure de la protection
    creation_date = models.DateTimeField(auto_now_add=True)

    # Date et heure d'expiration (par exemple, 7 jours après la création)
    expiration_date = models.DateTimeField()

    # Permet d'afficher une représentation lisible de l'objet
    def __str__(self):
        return f"ProtectedImage {self.original_filename} ({self.uuid})"

    # Un helper pour obtenir l'URL de l'image protégée
    def get_protected_image_url(self):
        return settings.MEDIA_URL + self.protected_image_path