# protection_app/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm

def upload_image_view(request):

    if request.method == 'GET':

        form = ImageUploadForm()

    return render(request, 'protection_app/upload_image.html', {'form': form})