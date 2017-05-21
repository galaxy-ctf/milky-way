from base.settings import *  # noqa

import os
import random
import string

if not os.path.exists('/tmp/django_secret'):
    with open('/tmp/django_secret', 'w') as handle:
        handle.write("".join([random.SystemRandom().choice(string.digits + string.punctuation) for i in range(100)]))

with open('/tmp/django_secret', 'r') as handle:
    SECRET_KEY = handle.read()

DEBUG = os.environ.get('DJANGO_DEBUG', None) == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
