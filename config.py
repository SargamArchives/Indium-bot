import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")
ID1 = int(os.environ.get("ID1"))
ID2 = int(os.environ.get("ID2"))

# General configuration for bot
DEFAULT_PREFIX = ">"
ACTIVITY_STATUS = [f"prefix: {DEFAULT_PREFIX}", "your activity"]
DEFAULT_EMBED_COLOR = 0x01A6FF