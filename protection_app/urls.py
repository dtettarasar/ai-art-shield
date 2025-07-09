# protection_app/urls.py

from django.urls import path
from . import views # Importe les vues de protection_app/views.py

urlpatterns = [
    # Cette route pointe vers la fonction 'upload_image_view' dans views.py
    # Elle sera accessible à la racine de votre site (ex: http://127.0.0.1:8000/)
    path('', views.upload_image_view, name='upload_image'),
]