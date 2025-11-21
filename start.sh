#!/bin/bash
set -e

echo "=========================================="
echo "Starting KIABA application setup..."
echo "=========================================="

# Exécuter les migrations
echo ""
echo "Step 1: Running database migrations..."
python manage.py migrate --noinput
if [ $? -eq 0 ]; then
    echo "✓ Migrations completed successfully"
else
    echo "✗ Migration failed!"
    exit 1
fi

# Créer le Site Django si nécessaire
echo ""
echo "Step 2: Setting up Django Site..."
python manage.py shell << 'PYTHON_EOF'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiaba.settings')
django.setup()

from django.contrib.sites.models import Site
from django.conf import settings

try:
    site, created = Site.objects.get_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "ci-kiaba.com",
            "name": "KIABA",
        }
    )
    if not created and site.domain != "ci-kiaba.com":
        site.domain = "ci-kiaba.com"
        site.name = "KIABA"
        site.save()
    print(f"✓ Site configured: {site.domain} (ID: {site.id})")
except Exception as e:
    print(f"✗ Error setting up site: {e}")
    import traceback
    traceback.print_exc()
PYTHON_EOF

# Vérifier la configuration
echo ""
echo "Step 3: Checking Django configuration..."
python manage.py check --deploy || {
    echo "⚠ Django check found some issues, but continuing..."
}

# Démarrer Gunicorn
echo ""
echo "=========================================="
echo "Starting Gunicorn server..."
echo "=========================================="
exec gunicorn kiaba.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info

