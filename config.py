import os

try:
    import dotenv
    dotenv.load_dotenv()
except:
    pass


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")
ID1 = int(os.environ.get("ID1"))
ID2 = int(os.environ.get("ID2"))