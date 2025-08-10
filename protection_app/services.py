# protection_app/services.py

import os
import uuid
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import UnidentifiedImageError

from django.utils import timezone

import logging # Importe le module de logging

# Initialise un logger pour ce module
logger = logging.getLogger(__name__)

from .models import ProtectedImage # Importe ton modèle
from img_data import Img_Data # Importe ta classe Img_Data

class Protection_App_Services:

    @staticmethod
    def process_and_protect_image(uploaded_image, protection_strength):

        """
        Traite une image téléchargée, applique la protection,
        la sauvegarde et enregistre ses métadonnées dans la base de données.

        Args:
            uploaded_image: Le fichier image téléchargé par l'utilisateur (UploadFile).
            protection_strength (float): La force de protection à appliquer.

        Returns:
            tuple: (ProtectedImage_instance, error_message)
                Retourne l'instance ProtectedImage si succès, None sinon.
                Retourne un message d'erreur si échec, None sinon.
        """

        logger.info("\n--- Début du traitement de l'image ---")

        try:

            # --- 1. Gérer le nom de fichier unique et les chemins ---
            # Génère un UUID unique pour le nom de base du fichier
            unique_filename_base = str(uuid.uuid4())

            # Récupère l'extension originale du fichier
            file_extension = os.path.splitext(uploaded_image.name)[1]

            # Nom complet du fichier original (ID unique + extension)
            original_filename_with_ext = f"{unique_filename_base}{file_extension}"

            # Nom complet du fichier protégé (ID unique + '_p' + extension)
            protected_filename_with_ext = f"{unique_filename_base}_p{file_extension}"

            # Chemins absolus de sauvegarde
            original_full_path = os.path.join(settings.MEDIA_ORIGINAL_DIR, original_filename_with_ext)
            protected_full_path = os.path.join(settings.MEDIA_PROTECTED_DIR, protected_filename_with_ext)

            # Chemins relatifs pour la base de données (sans MEDIA_ROOT)
            # On stocke le chemin relatif à MEDIA_ROOT
            original_relative_path = os.path.join('original', original_filename_with_ext)
            protected_relative_path = os.path.join('protected', protected_filename_with_ext)

            logger.info(f"Génération des chemins :")
            logger.info(f"  - Nom original: {uploaded_image.name}")
            logger.info(f"  - Chemin de l'original: {original_full_path}")
            logger.info(f"  - Chemin du protégé: {protected_full_path}")

            # --- 2. Sauvegarde de l'image originale uploadée ---
            fs_original = FileSystemStorage(location=settings.MEDIA_ORIGINAL_DIR)
            fs_original.save(original_filename_with_ext, uploaded_image)
            print(f"Sauvegarde de l'image originale réussie.")
            print(f"Chemin de la sauvegarde: {original_full_path}")

            # --- 3. Traitement de l'image avec Img_Data ---
            print("Début du processus de protection de l'image...")
            img_to_protect = Img_Data(original_full_path)
            img_to_protect.secure_image(dct_strength=float(protection_strength))

            # nom complet du fichier de sortie (image avec protection)
            img_to_protect.export_protected_image(output_path=protected_full_path)
            print(f"Protected image saved at: {protected_full_path}")
            print(f"Image protégée sauvegardée avec succès.")

            # --- 4. Enregistrement dans la base de données ---
            # Calcule la date d'expiration (ex: 7 jours après la création)
            # Tu peux ajuster cette durée selon tes besoins
            print("Début de l'enregistrement des métadonnées dans la base de données...")
            expiration_date = timezone.now() + datetime.timedelta(days=7)

            protected_image_instance = ProtectedImage.objects.create(
                uuid=unique_filename_base, # L'UUID est généré par défaut par models.UUIDField, mais on le passe explicitement ici
                original_filename=uploaded_image.name, # Nom original donné par l'utilisateur
                original_image_path=original_relative_path,
                protected_image_path=protected_relative_path,
                protection_strength=float(protection_strength),
                expiration_date=expiration_date
            )
            
            print(f"L'objet ProtectedImage a été créé avec succès dans la base de données.")
            print(f"  - UUID: {protected_image_instance.uuid}")
            print(f"  - Nom du fichier: {protected_image_instance.original_filename}")
            print(f"  - Chemin relatif du protégé: {protected_image_instance.protected_image_path}")
            print(f"  - Date d'expiration: {protected_image_instance.expiration_date}")

            print("--- Fin du traitement de l'image (SUCCÈS) ---\n")

            return protected_image_instance, None # Succès, retourne l'instance et pas d'erreur

        
        except (IOError, UnidentifiedImageError, ValueError, RuntimeError) as e:
            # Gère les erreurs de traitement d'image ou de conversion
            error_message = f"Impossible de charger ou traiter l'image : {e}"
            print(f"Error during image processing: {error_message}")
            return None, error_message # Échec, retourne None pour l'instance et le message d'erreur
        
        except Exception as e:
            # Gère toute autre erreur inattendue
            error_message = f"Une erreur inattendue est survenue : {e}"
            print(f"Unexpected error: {error_message}")
            return None, error_message
        
        pass