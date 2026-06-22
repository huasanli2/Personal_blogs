#!/usr/bin/env bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating initial users if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='user1').exists():
    u1 = User.objects.create_user(username='user1', password='change-me-1', nickname='宝宝')
    u1.is_staff = True
    u1.is_superuser = True
    u1.save()
    print('Created user1 (admin)')
if not User.objects.filter(username='user2').exists():
    u2 = User.objects.create_user(username='user2', password='change-me-2', nickname='贝贝')
    print('Created user2')
"

echo "Build complete!"
