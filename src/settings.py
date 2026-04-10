import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

DOTENV_DIR = BASE_DIR.parent / ".env"
if not load_dotenv(DOTENV_DIR):
    logger.warning("Not found env file in %s", DOTENV_DIR)

MONGODB_URI = os.environ["MONGODB_URI"]
