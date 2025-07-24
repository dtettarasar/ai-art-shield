# Makefile
# Raccourcis pour les commandes du projet Django avec Docker

# Lancer les conteneurs en mode détaché (pour la production ou l'environnement de test sur serveur)
# Utilisation : make docker-up-prod
docker-up-prod:
	docker compose up -d

# Lancer les conteneurs et afficher les logs (pour le développement local)
# Utilisation : make docker-up-dev
docker-up-dev:
	docker compose up

# Arrêter et supprimer les conteneurs
# Utilisation : make docker-down
docker-down:
	docker compose down

# Lancer le serveur de développement Django à l'intérieur du conteneur (pour le debug)
# Utilisation : make runserver
# Note : Cette commande est principalement utile si tu as lancé docker-up-prod et que tu veux voir les logs du serveur web spécifiquement
runserver:
	docker compose logs -f web

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