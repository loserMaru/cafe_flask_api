import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# Настройки базы данных
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_TRACK_MODIFICATIONS = False  # получаем URL базы данных из переменной окружения
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# Настройки безопасности и аутентификации
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Другие настройки приложения
FLASK_DEBUG = int(os.getenv("FLASK_DEBUG"))  # Включаем отладочный режим, если DEBUG=True
PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_AUTH_HEADER_PREFIX = os.getenv("JWT_AUTH_HEADER_PREFIX")
