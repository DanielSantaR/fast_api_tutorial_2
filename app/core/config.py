import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/core/enviroment/.env_app")

API_STR = f"/api"
SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")
PROJECT_NAME = os.getenv("PROJECT_NAME")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
