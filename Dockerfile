# Utilise une image Python officielle comme base, version Alpine pour la légèreté
FROM python:3.12-alpine

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de configuration des dépendances (pyproject.toml et uv.lock)
# avant d'installer les dépendances pour optimiser le cache Docker.
COPY pyproject.toml uv.lock ./

# Installe les dépendances système nécessaires pour psycopg2-binary et d'autres paquets
# 'postgresql-dev' fournit les en-têtes nécessaires pour compiler psycopg2
# 'gcc' et 'musl-dev' sont des outils de compilation de base sur Alpine
# 'libffi-dev' est parfois nécessaire pour d'autres packages comme cryptography
# 'jpeg-dev', 'zlib-dev', 'freetype-dev', 'lcms2-dev', 'tiff-dev', 'tk-dev'
# sont nécessaires pour Pillow si tu utilises des fonctionnalités d'image avancées.
RUN apk update && \
    apk add --no-cache postgresql-dev gcc musl-dev libffi-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev tiff-dev tk-dev && \
    # Nettoie le cache apk pour réduire la taille de l'image
    rm -rf /var/cache/apk/*

# Installe 'uv' globalement, puis utilise 'uv sync' pour installer les dépendances du projet
# en se basant sur uv.lock pour des installations reproductibles.
RUN pip install uv && uv sync --locked

# Copie le reste du code du projet dans le répertoire de travail
COPY . .

# Indique à Docker que l'application écoute sur le port 8000
EXPOSE 8000

# Commande par défaut pour lancer le serveur.
# Note: Cette commande peut être surchargée par la directive 'command' dans docker-compose.yml.
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
