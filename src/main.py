from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]
ENV_FILE = ROOT_DIR / ".env"

if not ENV_FILE.exists():
    print(f"Missing .env file in {ROOT_DIR}")
else:
    load_dotenv(ENV_FILE.absolute().as_posix())
    print(f"Loading environment variables from {ENV_FILE}")


from app.api import *

import logging

logging.basicConfig(level=logging.INFO)
