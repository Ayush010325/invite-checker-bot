import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("Token")
INVITE_CHANNEL_ID = int(os.getenv("INVITE_CHANNEL_ID"))