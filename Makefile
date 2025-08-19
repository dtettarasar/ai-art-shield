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

# Construire et relancer les conteneurs (avec reconstruction de l'image si des changements ont été faits dans le Dockerfile ou le code)
# Utilisation : make docker-build
docker-build:
	docker compose up -d --build

# Arrêter et supprimer les conteneurs
# Utilisation : make docker-down
docker-down:
	docker compose down

# Lancer le serveur de développement Django à l'intérieur du conteneur (pour le debug)
# Utilisation : make runserver
# Note : Cette commande est principalement utile si tu as lancé docker-up-prod et que tu veux voir les logs du serveur web spécifiquement
runserver:
	docker compose logs -f web

# Redémarrer le conteneur du serveur web pour appliquer les changements de code
# Utilisation : make restart-server
restart-server:
	docker compose restart web

# Créer de nouvelles migrations basées sur les changements de modèles (pour la protection_app)
# Utilisation : make makemigrations-protection-app
makemigrations-protection-app:
	docker compose exec web uv run python manage.py makemigrations protection_app

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

# --- Commandes de nettoyage ---

# Nettoyer les volumes de données Docker non utilisés
# Utilisation : make clean-volumes
clean-volumes:
	docker volume prune

# Nettoyer les images Docker non utilisées par des conteneurs
# Utilisation : make clean-images
clean-images:
	docker image prune -a

# Nettoyage complet de l'environnement Docker (supprime tout ce qui n'est pas utilisé, y compris les conteneurs, volumes et images)
# Utilisation : make clean-all
clean-all:
	docker system prune -a --volumes

.PHONY: docker-up-prod docker-up-dev docker-build docker-down runserver restart-server makemigrations-protection-app migrate test install clean-volumes clean-images clean-all
