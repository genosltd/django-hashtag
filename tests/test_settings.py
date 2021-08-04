SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "test_app",
    "django_hashtag",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}

