# protection_app/views.py

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from PIL import UnidentifiedImageError

from .forms import ImageUploadForm

import uuid # pour générer des IDs uniques

import os

from img_data import Img_Data

def upload_image_view(request):

    """
    Gère l'upload d'image, l'application du filigrane
    et l'affichage de l'image protégée.
    """

    protected_image_url = None # Initialise à None pour le contexte du template

    if request.method == 'GET':

        form = ImageUploadForm()

    elif request.method == 'POST':

        print('post request from image upload form')

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            # Récupérer l'image et la force de protection
            uploaded_image = form.cleaned_data['image']
            protection_strength = form.cleaned_data['strength']

            print("uploaded_image: ")
            print(uploaded_image)

            print("protection_strength: ")
            print(protection_strength)

            # --- 1. Gérer le nom de fichier unique et les chemins ---
            # Génère un UUID unique pour le nom de base du fichier
            unique_filename_base = str(uuid.uuid4())

            # Récupère l'extension originale du fichier
            file_extension = os.path.splitext(uploaded_image.name)[1]

            # Nom complet du fichier original (ID unique + extension)
            original_filename_with_ext = f"{unique_filename_base}{file_extension}"

            # Nom complet du fichier protégé (ID unique + '_p' + extension)
            protected_filename_with_ext = f"{unique_filename_base}_p{file_extension}"

            # Définir le chemin de sauvegarde de l'image originale
            original_file_path = os.path.join(settings.MEDIA_ORIGINAL_DIR, original_filename_with_ext)

            # Définir le chemin de sauvegarde de l'image protégée (utilisé par Img_Data)
            # Img_Data aura besoin du répertoire de sortie et du nom de fichier souhaité
            protected_file_output_dir = settings.MEDIA_PROTECTED_DIR

            # --- 2. Sauvegarde de l'image originale uploadée ---
            # Utilise un gestionnaire de stockage pour sauvegarder le fichier
            fs = FileSystemStorage(location=settings.MEDIA_ORIGINAL_DIR)
            fs.save(original_filename_with_ext, uploaded_image) # Sauvegarde l'image dans le dossier 'original'

            print(f"Original image saved at: {original_file_path}")

            # --- 3. Traitement de l'image avec Img_Data ---

            img_to_protect = None

            try:

                img_to_protect = Img_Data(original_file_path)

                print(img_to_protect)

                #float(protection_strength)

                img_to_protect.secure_image(dct_strength=float(protection_strength))
            
            except (IOError, UnidentifiedImageError, ValueError, RuntimeError) as e:

                # Si l'image ne peut pas être chargée ou identifiée par Img_Data
                # Ajoute l'erreur au formulaire pour l'afficher à l'utilisateur
                form.add_error(None, f"Impossible de charger ou traiter l'image : {e}")

                # print(e)

                # Rendre le template avec le formulaire et l'erreur
                # Il est important de retourner le rendu ici pour arrêter le traitement du POST
                return render(request, 'protection_app/upload_image.html', {'form': form})
            
            finally:
                # Nettoyer l'image originale uploadée si tu ne veux pas la garder.
                # Dans notre cas, on la garde dans le dossier 'original'.
                pass # Ne rien faire ici si tu conserves l'original


        else:
            # Si le formulaire n'est pas valide (ex: mauvais type de fichier, force hors limites)
            # Le template affichera automatiquement les erreurs via {{ form.errors }} ou {{ field.errors }}
            pass

    return render(request, 'protection_app/upload_image.html', {'form': form})