# Django commands using uv

# Run the development server (default port 8000)
run port='8000':
    uv run python manage.py runserver {{port}}

# Run database migrations
migrate:
    uv run python manage.py migrate

# Create migration files
mm app='':
    uv run python manage.py makemigrations {{app}}

# Show migration status
showmigrations:
    uv run python manage.py showmigrations

# Create a superuser
createsuperuser:
    uv run python manage.py createsuperuser

# Open Django shell with shell_plus and ipython
shell:
    uv run python manage.py shell_plus --ipython

# Run tests with pytest
test:
    uv run pytest

# Run tests for specific app
test-app app='blog':
    uv run pytest {{app}}/

# Run tests with coverage
test-cov:
    uv run pytest --cov=. --cov-report=html

# Collect static files
collectstatic:
    uv run python manage.py collectstatic --noinput

# Show all Django management commands
help:
    uv run python manage.py help

# Check for common problems
check:
    uv run python manage.py check

# Show SQL for migrations (dry run)
sqlmigrate app migration:
    uv run python manage.py sqlmigrate {{app}} {{migration}}

# Flush the database (remove all data)
flush:
    uv run python manage.py flush --noinput

# Show URL patterns
showurls:
    uv run python manage.py showurls

# Run database shell
dbshell:
    uv run python manage.py dbshell

# Make migrations and migrate in one command
mmm app='':
    uv run python manage.py makemigrations {{app}}
    uv run python manage.py migrate

# Run pre-commit hooks on all files
pre-commit:
    uv run pre-commit run --all-files

# Show SQL for a queryset (usage: just sql "Artigo.objects.all()")
sql query='':
    uv run python manage.py shell -c "from blog.models import Artigo, Comentario; from django.db import connection; qs = {{query}}; print('SQL:', qs.query); print('Params:', qs.query.params)"
