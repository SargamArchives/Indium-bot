import os
import dotenv

dotenv.load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
ID1 = int(os.getenv("ID1"))
ID2 = int(os.getenv("ID2"))