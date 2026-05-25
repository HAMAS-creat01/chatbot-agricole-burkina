import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DATABASE = "database/agriculteur.db"
    DEBUG = True