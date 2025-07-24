# protection_app/views.py

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

# from django.core.files.storage import FileSystemStorage

# from PIL import UnidentifiedImageError

from .forms import ImageUploadForm

# import uuid # pour générer des IDs uniques

# import os

# from img_data import Img_Data

from .services import Protection_App_Services

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

            # Appelle la méthode statique directement sur la classe
            protected_image_instance, error_message = Protection_App_Services.process_and_protect_image(
                uploaded_image,
                protection_strength
            )

            if protected_image_instance:
                # Succès: utilise l'instance retournée pour obtenir l'URL
                protected_image_url = protected_image_instance.get_protected_image_url()
                print(f"Protected image URL for display: {protected_image_url}")
            else:
                # Échec: ajoute l'erreur au formulaire pour l'affichage
                form.add_error(None, error_message)
                print(f"Error in view: {error_message}")

            # --- Mettre à jour le contexte et rendre la page ---
            context = {
                'form': form,
                'protected_image_url': protected_image_url
            }

            # La page est rendue ici avec l'URL de l'image pour affichage
            return render(request, 'protection_app/upload_image.html', context)


        else:
            # Si le formulaire n'est pas valide (ex: mauvais type de fichier, force hors limites)
            # Le template affichera automatiquement les erreurs via {{ form.errors }} ou {{ field.errors }}
            pass

    return render(request, 'protection_app/upload_image.html', {'form': form})