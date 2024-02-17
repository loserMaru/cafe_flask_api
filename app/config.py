import os

from dotenv import load_dotenv

load_dotenv()

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL")  # получаем URL базы данных из переменной окружения
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Настройки безопасности и аутентификации
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Другие настройки приложения
FLASK_DEBUG = os.getenv("FLASK_DEBUG")  # Включаем отладочный режим, если DEBUG=True

# Дополнительные настройки, такие как настройки веб-сервера, кэширования и т. д.
