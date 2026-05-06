#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from accounts.models import User

admin, created = User.objects.get_or_create(username='admin1')
admin.email = 'admin@test.com'
admin.role = 'admin'
admin.is_staff = True
admin.is_superuser = True
admin.set_password('buhara2026')
admin.save()

worker, created = User.objects.get_or_create(username='worker1')
worker.role = 'worker'
worker.set_password('worker2026')
worker.save()

reviewer, created = User.objects.get_or_create(username='reviewer1')
reviewer.role = 'reviewer'
reviewer.set_password('reviewer2026')
reviewer.save()
"