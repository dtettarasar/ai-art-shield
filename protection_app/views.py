# protection_app/views.py

from django.shortcuts import render
from django.http import HttpResponse

def upload_image_view(request):
    """
    Vue pour afficher la page d'upload d'image.
    Pour l'instant, elle retourne juste un message simple.
    """
    return HttpResponse("Bienvenue sur la page de protection d'image ! Le formulaire sera ici.")