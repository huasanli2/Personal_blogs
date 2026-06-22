#!/usr/bin/env bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating and updating users..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
for uname, nick, staff in [('user1', '宝宝', True), ('user2', '贝贝', False)]:
    u, created = User.objects.get_or_create(username=uname, defaults={'nickname': nick, 'is_staff': staff, 'is_superuser': staff})
    u.set_password('123456')
    u.save()
EOF

echo "Starting server..."
exec daphne config.asgi:application --port $PORT --bind 0.0.0.0
