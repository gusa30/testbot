# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:54:35 2025

@author: User
"""

import os
import asyncio
from twitchio.ext import commands
from discord import Intents, Client
from dotenv import load_dotenv

# 讀取 .env 環境變數
load_dotenv()

# Twitch
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL")
TARGET_USER = os.getenv("TARGET_USER").lower()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# 建立 Twitch Bot
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix='!',
            initial_channels=[TWITCH_CHANNEL]
        )

    async def event_ready(self):
        print(f"Twitch bot is ready. Monitoring #{TWITCH_CHANNEL}.")

    async def event_message(self, message):
        if message.author.name.lower() == TARGET_USER:
            msg = f"[{message.author.name}] {message.content}"
            print(f"捕捉到：{msg}")
            await send_to_discord(msg)

# 建立 Discord Client
intents = Intents.default()
intents.messages = True

discord_client = Client(intents=intents)

async def send_to_discord(content):
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(content)
    else:
        print("❌ 無法找到 Discord 頻道")

# 啟動兩個 bot
async def main():
    twitch_bot = TwitchBot()
    await asyncio.gather(
        twitch_bot.start(),
        discord_client.start(DISCORD_TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
