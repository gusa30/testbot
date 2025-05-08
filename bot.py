# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:08:45 2025

@author: User
"""

import os
import asyncio
from twitchio.ext import commands
import discord
from discord.ext import commands as discord_commands
from datetime import datetime
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

# 環境變數
TWITCH_TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
TWITCH_CHANNELS = os.getenv("TWITCH_CHANNELS").split(",")
TARGET_USERS = set([u.strip().lower() for u in os.getenv("TARGET_USERNAMES").split(",")])
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# --- Twitch Bot ---
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix="!", initial_channels=TWITCH_CHANNELS)

    async def event_ready(self):
        print(f"[Twitch] Bot 已登入為: {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        username = message.author.name.lower()
        if username in TARGET_USERS:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            msg = f"{timestamp} @{username} 在 #{message.channel.name} 說：{message.content}"
            print(msg)
            await send_to_discord(msg)

# --- Discord Bot 客戶端（只負責傳訊息） ---
discord_client = discord.Client(intents=discord.Intents.default())

async def send_to_discord(content):
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(content)

# --- 同時啟動 Twitch 和 Discord ---
async def main():
    twitch_bot = TwitchBot()

    # 並行執行 Twitch bot 和 Discord bot
    await asyncio.gather(
        discord_client.start(DISCORD_TOKEN),
        twitch_bot.start()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot 已手動停止。")
