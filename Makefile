# Makefile
# Raccourcis pour les commandes du projet Django avec Docker

# Lancer les conteneurs en mode détaché
# Utilisation : make docker-up
docker-up:
	docker compose up -d

# Arrêter et supprimer les conteneurs
# Utilisation : make docker-down
docker-down:
	docker compose down

# Lancer le serveur de développement Django à l'intérieur du conteneur
# Utilisation : make runserver
runserver:
	docker compose exec web uv run python manage.py runserver 0.0.0.0:8000

# Lancer les migrations à l'intérieur du conteneur
# Utilisation : make migrate
migrate:
	docker compose exec web uv run python manage.py migrate

# Exécuter les tests à l'intérieur du conteneur
# Utilisation : make test
test:
	docker compose exec web uv run pytest

# Installer ou synchroniser les dépendances du projet
# Cette commande est maintenant gérée par le Dockerfile, mais elle peut être utile pour l'environnement local
# Utilisation : make install
install:
	uv sync