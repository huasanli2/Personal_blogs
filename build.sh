#!/usr/bin/env bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating and updating users..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
for uname, nick, staff in [('user1', '\u5b9d\u5b9d', True), ('user2', '\u8d1d\u8d1d', False)]:
    u, created = User.objects.get_or_create(username=uname, defaults={'nickname': nick, 'is_staff': staff, 'is_superuser': staff})
    u.set_password('123456')
    u.save()
"

echo "Starting server..."
exec daphne config.asgi:application --port $PORT --bind 0.0.0.0
