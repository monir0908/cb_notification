import os
from pyfcm import FCMNotification

DEBUG = os.environ.get('DEBUG')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL')
REDIS_HOST = os.environ.get('REDIS_HOST')
MONGO_URL = os.environ.get('MONGO_URL')
SENTRY_DSN = os.environ.get('SENTRY_DSN')
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
ACCESS_TOKEN_SECRET_KEY = os.environ.get('ACCESS_TOKEN_SECRET_KEY')
ACCESS_TOKEN_EXPIRY = 10  # 10 hour
REFRESH_TOKEN_SECRET_KEY = os.environ.get('REFRESH_TOKEN_SECRET_KEY')
REFRESH_TOKEN_EXPIRY = 7  # 7 days
V1_PATTERNS = '/api/v1.0'
FCM_KEY = os.environ.get('FCM_KEY')
push_service = FCMNotification(api_key=FCM_KEY)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
}
COUNTRY_CODE_MAP = {
    'bd', '88'
}
CORS_ALLOW_ORIGINS = ['*']
