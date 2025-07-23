# Dockerfile

# Utilise une image Python officielle comme base
FROM python:3.12-alpine

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de configuration des dépendances pour l'installation
COPY pyproject.toml uv.lock ./

# Installe les dépendances du projet en utilisant uv
RUN pip install uv && uv sync --locked

# Copie le reste du code du projet
COPY . .

# Indique à Docker que l'application écoute sur le port 8000
EXPOSE 8000

# Commande par défaut pour lancer le serveur
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]