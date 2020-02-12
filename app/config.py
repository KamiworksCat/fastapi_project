"""
Configurations for this fast api project
"""
import os

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)
API_PREFIX = "/api/v1"

SECRET_KEY = "4bb8aeba6dfed3281a19f26f0527f35ffe4015b1025f77329367ef0e37d4efe5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

FIRST_SUPERUSER = "adminuser@email.com"
FIRST_SUPERUSER_PASSWORD = "adminuser"

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
