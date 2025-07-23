# Makefile
# Raccourcis pour les commandes du projet Django avec uv

# Lancer le serveur de développement Django
# Utilisation : make runserver
runserver:
	uv run python manage.py runserver

# Lancer les migrations
# Utilisation : make migrate
migrate:
	uv run python manage.py migrate

# Installer ou synchroniser les dépendances du projet
# Utilisation : make install
install:
	uv sync

# Exécuter les tests
# Utilisation : make test
test:
	uv run pytest