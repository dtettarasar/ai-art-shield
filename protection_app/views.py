# protection_app/views.py

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import ImageUploadForm

import os

def upload_image_view(request):

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

            # A checker avant : MEDIA_ROOT doit être configuré dans settings.py
            # Sinon, cette partie échouera.
            fs = FileSystemStorage()

            # Nommer le fichier de manière unique pour éviter les conflits
            uploaded_filename = fs.save(uploaded_image.name, uploaded_image)
            uploaded_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_filename)

            print("uploaded_filename: ")
            print(uploaded_filename)

            print("uploaded_file_path: ")
            print(uploaded_file_path)


        else:
            # Si le formulaire n'est pas valide (ex: mauvais type de fichier, force hors limites)
            # Le template affichera automatiquement les erreurs via {{ form.errors }} ou {{ field.errors }}
            pass

    return render(request, 'protection_app/upload_image.html', {'form': form})