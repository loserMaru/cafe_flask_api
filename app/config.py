import os

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
JWT_EXPIRATION_DELTA = int(os.getenv("JWT_EXPIRATION_DELTA")) * 24 * 60 * 60
# Дополнительные настройки, такие как настройки веб-сервера, кэширования и т. д.
JWT_AUTH_HEADER_PREFIX = os.getenv("JWT_AUTH_HEADER_PREFIX")
