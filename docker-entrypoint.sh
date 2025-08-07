#!/bin/sh

# Ce script configure et démarre l'application Django.
# C'est le point d'entrée pour le conteneur Docker.

# Change le répertoire de travail vers la racine du projet.
# Cela garantit que Python peut trouver les fichiers du projet.
cd /app

# Exécute les migrations Django en utilisant l'environnement géré par uv.
echo "Exécution des migrations..."
uv run python manage.py makemigrations
uv run python manage.py migrate
echo "Migrations terminées."

# Démarre le serveur Gunicorn en utilisant l'environnement géré par uv.
# La commande Gunicorn référence correctement le dossier du projet `ai_art_shield_project`.
echo "Démarrage du serveur Gunicorn..."
uv run gunicorn --bind 0.0.0.0:8000 --chdir=/app ai_art_shield_project.wsgi:application
