from pathlib import Path
import os
from datetime import timedelta
# import environ
DJANGO_SETTINGS_MODULE='handsup.settings'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

DP_MODE = True # 배포 모드 설정 Deploy_Mode

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secret') if DP_MODE else 'secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if DP_MODE else True


ALLOWED_HOSTS = ['backend'] if DP_MODE else ['*']

# goods(auction) user community review?
# Application definition

INSTALLED_APPS = [
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # service app
    'user',
    'review',
    'chat',
    'board',
    # 'auction',
    'goods',

    # django
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',

    # CORS provider
    # 'corsheaders',

    # crontab
    'django_crontab',

    # Router
    'channels',


]

# Channels

ASGI_APPLICATION = 'handsup.asgi.application'

WSGI_APPLICATION = 'handsup.wsgi.application'

if DP_MODE:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('redis', 6379)],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'handsup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


POSTGRES_DB = os.environ.get('POSTGRES_DB', '') if DP_MODE else False

if POSTGRES_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': os.environ.get('POSTGRES_USER', ''),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', ''),
            'PORT': os.environ.get('POSTGRES_PORT', ''),
        }
    }
# 환경변수가 존재하지 않을 경우 sqlite3을 사용합니다.
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

# Media files (Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CORS
# live server port 5500
CORS_ORIGIN_WHITELIST = ['http://hands-up.co.kr', 'http://43.200.179.49', 'http://backend.hands-up.co.kr']
# 예외 없이 다 수락
CORS_ALLOW_CREDENTIALS = False if DP_MODE else True
CORS_ALLOW_ALL_ORIGINS = False if DP_MODE else True
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=10000),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CRONTAB_DJANGO_SETTINGS_MODULE='handsup.settings'
#CRONTAB_DJANGO_SETTINGS_MODULE= os.path.join(BASE_DIR, 'handsup.settings')
# crontab
CRONJOBS = [
    # 매주 월요일 새벽 1시 매너점수 반영, 비매너 유저 제재
    ('0 1 * * 1', 'review.cron.anonymous_review', '>> '+os.path.join(BASE_DIR, 'handsup/log/cron.log')+' 2>&1 '),
    # 매일 자정 비매너 유저 제재 풀기
    ('0 0 * * *', 'review.cron.prison_break', '>> '+os.path.join(BASE_DIR, 'handsup/log/cron.log')+' 2>&1 '),
    # 4개월 마다 점수 리셋
    ('0 0 1 */3 *', 'review.cron.rating_score_reset', '>> '+os.path.join(BASE_DIR, 'handsup/log/cron.log')+' 2>&1 '),
    # 매분
    ('* * * * *', 'goods.cron.auction_start_and_end', '>> '+os.path.join(BASE_DIR, 'handsup/log/cron.log')+' 2>&1 '),
    # ('* * * * *', 'goods.cron.test', '>> '+os.path.join(BASE_DIR, 'handsup/log/cron.log')+' 2>&1 '),
]


# LOGGING = {
#     'version': 1,	#logging 버젼
#     'disable_existing_loggers': False, # 원래 있던 로깅들을 그래도 냅둠 # 만약 True면 못쓴다는 거겠죠? ㅎ
#     'handlers': {					# 로깅 메세지에서 일어나는 일을 결정하는 녀석이라고 장고공식문서에 나와있는데, 아직 무슨말인지는 저도 모르겠네요 ㅎㅎ
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {				# 로깅을 console에 띄울지 ... 다른데 띄울지 그냥 DEBUG용으로 레벨을 설정할 수 도있고,
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }