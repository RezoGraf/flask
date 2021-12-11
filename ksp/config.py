from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
DB_CONFIG = environ.get('DB_CONFIG')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_CHARSET = environ.get('DB_CHARSET')
