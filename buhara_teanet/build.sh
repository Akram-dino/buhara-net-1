#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate


python manage.py shell -c "
from accounts.models import User;

if not User.objects.filter(username='admin1').exists():
    User.objects.create_superuser(
        username='admin1',
        email='admin@test.com',
        password='Admin12345'
    );

if not User.objects.filter(username='worker1').exists():
    User.objects.create_user(
        username='worker1',
        password='Worker12345',
        role='worker'
    );

if not User.objects.filter(username='reviewer1').exists():
    User.objects.create_user(
        username='reviewer1',
        password='Reviewer12345',
        role='reviewer'
    );
"