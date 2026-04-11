import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Configure basic logging with INFO level
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from the .env file
DOTENV_DIR = BASE_DIR.parent / ".env"
if not load_dotenv(DOTENV_DIR):
    _logger.warning("Not found env file in %s", DOTENV_DIR)

# MongoDB connection
DB_URI = os.environ["DB_URI"]
DB_NAME = os.environ["DB_NAME"]

# JWT setup
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE = timedelta(days=60)
