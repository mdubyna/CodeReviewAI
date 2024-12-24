import os

from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FILES_FOR_REVIEWING = tuple(os.getenv("FILES_FOR_REVIEWING").split(","))
EXCLUDED_FILE_NAMES = os.getenv("EXCLUDED_FILE_NAMES")
EXCLUDED_DIR_NAMES = os.getenv("EXCLUDED_DIR_NAMES")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")