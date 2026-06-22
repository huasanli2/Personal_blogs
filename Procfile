web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='user1').exists():
    User.objects.create_user('user1', 'change-me-1', nickname='宝宝', is_staff=True, is_superuser=True)
    print('Created user1')
if not User.objects.filter(username='user2').exists():
    User.objects.create_user('user2', 'change-me-2', nickname='贝贝')
    print('Created user2')
" && daphne config.asgi:application --port $PORT --bind 0.0.0.0
