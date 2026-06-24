import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

os.environ.setdefault("U2NET_HOME", str(Path(__file__).parent / ".cache" / "u2net"))

import discord
from commands import COMMANDS

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    handler = COMMANDS.get(message.content)
    if handler:
        await handler(message)


client.run(os.environ["DISCORD_TOKEN"])
