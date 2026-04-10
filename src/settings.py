import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

DOTENV_DIR = BASE_DIR.parent / ".env"
if not load_dotenv(DOTENV_DIR):
    logger.warning("Not found env file in %s", DOTENV_DIR)

MONGODB_URI = os.environ["MONGODB_URI"]

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE = timedelta(days=60)
