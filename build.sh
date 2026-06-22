#!/usr/bin/env bash
set -e

echo "=== Diagnostic Info ==="
echo "Current user: $(whoami) (ID: $(id -u))"
echo "Checking /app/media permissions:"
ls -ld /app/media || echo "/app/media does not exist"
echo "Testing write to /app/media..."
if touch /app/media/write_test 2>/dev/null; then
    echo "Write test successful!"
    rm /app/media/write_test
else
    echo "Write test FAILED! /app/media is NOT writable by $(whoami)."
fi
echo "======================="

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
