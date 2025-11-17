import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = env('SECRET_KEY', default='unsafe-secret-key')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary apps
    'cloudinary',
    'cloudinary_storage',

    'delivery',
]

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # Required for Render static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meal_buddy.urls'

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meal_buddy.wsgi.application'

# ---------------- DATABASE ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- PASSWORD VALIDATION ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- TIME & LANGUAGE ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------
STATIC_URL = '/static/'

# Where your static folder is located  
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Where collectstatic dumps files (Render will serve this)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Required for serving CSS/JS on Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------- CLOUDINARY MEDIA STORAGE ----------------
# Cloudinary stores all uploaded images
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

# Do NOT use MEDIA_URL for Cloudinary
MEDIA_URL = '/media/'  # kept to avoid breaking templates, but Cloudinary overrides actual usage

# ---------------- RAZORPAY ----------------
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='rzp_test_RPInetkpqOv0Pv')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='zt3tc4fxUUF9uRoF2RkncZqy')

if DEBUG:
    print("DEBUG MODE ON — Razorpay:", RAZORPAY_KEY_ID)
