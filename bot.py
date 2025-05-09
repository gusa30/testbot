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
from flask import Flask
from threading import Thread

# 載入 .env 檔案中的環境變數
load_dotenv()

# --- 請在 .env 檔中設定以下變數 ---
# TWITCH_TOKEN:     你的 Twitch IRC OAuth Token（格式為 oauth:xxxxx）
# TWITCH_NICK:      你的 Twitch 使用者名稱（機器人帳號）
# TWITCH_CHANNELS:  要監控的頻道們，用逗號分隔（例：channel1,channel2）
# TARGET_USERS:     要追蹤的特定使用者名稱（可多個，逗號分隔）
# DISCORD_TOKEN:    Discord Bot Token
# DISCORD_CHANNEL_ID: 要轉發訊息的 Discord 頻道 ID（數字）

TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
TWITCH_NICK = os.getenv("TWITCH_NICK")
TWITCH_CHANNELS = os.getenv("TWITCH_CHANNELS").split(',')
TARGET_USERS = [user.strip().lower() for user in os.getenv("TARGET_USERS").split(',')]
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Discord 客戶端設定
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix='!',
            initial_channels=TWITCH_CHANNELS
        )

    async def event_ready(self):
        print(f'Logged into Twitch as | {self.nick}')

    async def event_message(self, message):
        # 忽略自己的訊息
        if message.author.name.lower() == TWITCH_NICK.lower():
            return

        if message.author.name.lower() in TARGET_USERS:
            content = f"[{message.channel.name}] {message.author.name}: {message.content}"
            print(content)
            await send_to_discord(content)

# 發送訊息到 Discord
async def send_to_discord(message):
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("無法找到指定的 Discord 頻道")

# 小型 Flask Web Server 用來保持 Render/Replit 運作
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# 程式進入點
if __name__ == "__main__":
    keep_alive()
    twitch_bot = TwitchBot()

    loop = asyncio.get_event_loop()
    loop.create_task(twitch_bot.start())
    loop.create_task(discord_client.start(DISCORD_TOKEN))
    loop.run_forever()

