# 구글 서비스
import os
from pathlib import Path
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # 프로젝트 루트 디렉터리 경로
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-s0o2jzdy#nizj)c3(j*2bs#bzc_2a5c@fq+3%g3yw_()t6p@in'
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',     # 구글 스토리지
    'music',  # 앱
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'musicgenerator.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'music/templates'],
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

WSGI_APPLICATION = 'musicgenerator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'music', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic으로 파일이 수집될 디렉토리

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# GCS를 사용할 경우, `DEBUG=False` 상태에서만 적용
if not DEBUG:
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # STATIC_BUCKET_NAME = os.environ.get('STATIC_BUCKET_NAME', 'andong-24-team-101-staticfiles')
    STATIC_BUCKET_NAME = 'andong-24-team-101-staticfiles'
    STATIC_URL = f'https://storage.googleapis.com/{STATIC_BUCKET_NAME}/static/'

# 미디어 파일(업로드 파일)용 버킷 설정
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
MEDIA_BUCKET_NAME = os.environ.get('MEDIA_BUCKET_NAME', 'test_music_team_101')
MEDIA_URL = f'https://storage.googleapis.com/{MEDIA_BUCKET_NAME}/test_image/'

# 로컬 환경에서는 서비스 계정 키 파일 사용
if os.getenv('GAE_ENV', '').startswith('standard'):
    GS_CREDENTIALS = None  # GCP에서 실행 시 기본 자격 증명을 사용
else:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'service-account-key.json')
    )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-eq9bPDW6Rs8BoOq0hPNRUnRdf88KJDtCuryo5vXE59T3BlbkFJQZhCWQwt9D_mIMCEnNX5JmzqxOBpJd1-CknVGQoLoA')

# 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