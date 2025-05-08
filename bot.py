# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:54:35 2025

@author: User
"""

import os
import asyncio
from twitchio.ext import commands
import discord
from dotenv import load_dotenv

# 載入 .env 檔案中的變數
load_dotenv()

# 讀取環境變數
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
TWITCH_NICK = os.getenv("TWITCH_NICK")
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL")
TARGET_USER = os.getenv("TARGET_USER").lower()

# 建立 Discord Bot
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

# Twitch Bot
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix='!',
                         initial_channels=[TWITCH_CHANNEL])

    async def event_ready(self):
        print(f'🟣 Twitch Bot 已登入：{self.nick}')

    async def event_message(self, message):
        if message.author.name.lower() == TARGET_USER:
            content = f"[{message.channel.name}] {message.author.name}: {message.content}"
            print(content)
            await send_to_discord(content)

# 傳送訊息到 Discord 頻道
async def send_to_discord(message):
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

# 同時啟動 Twitch 和 Discord bot
async def main():
    twitch_bot = TwitchBot()
    await asyncio.gather(
        twitch_bot.start(),
        discord_client.start(DISCORD_TOKEN)
    )

# 執行主程式
if __name__ == "__main__":
    asyncio.run(main())
