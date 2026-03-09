import discord
from discord.ext import commands
import config
import database   # ← add this

from modules.tracker import setup_tracker
from modules.verifier import setup_verifier
from modules.scanner import setup_scanner

# create database + table
database.setup_database()   # ← add this

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

# load modules
setup_tracker(bot)
setup_verifier(bot)
setup_scanner(bot)

try:
    bot.run(config.TOKEN)
except Exception as e:
    print("Bot failed to start:", e)