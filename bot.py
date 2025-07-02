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

load_dotenv()

# 載入環境變數
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
TWITCH_NICK = os.getenv("TWITCH_NICK")
TWITCH_CHANNELS = [c.strip() for c in os.getenv("TWITCH_CHANNELS", "").split(",")]
TARGET_USERS = [u.strip().lower() for u in os.getenv("TARGET_USERS", "").split(",")]
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Discord bot 初始化
discord_intents = discord.Intents.default()
discord_client = discord.Client(intents=discord_intents)

# Twitch bot（v2）
class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=TWITCH_CHANNELS
        )

    async def event_ready(self):
        print(f"✅ Twitch Bot logged in as: {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return  # 忽略自己的訊息

        if message.author.name.lower() in TARGET_USERS:
            msg = f"[{message.channel.name}] {message.author.name}: {message.content}"
            print(msg)
            await send_to_discord(msg)

# 發送訊息到 Discord 頻道
async def send_to_discord(content):
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(content)
    else:
        print("❗ 無法找到 Discord 頻道")

# Flask keep-alive server（給 UptimeRobot）
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_web).start()

# 主程式入口
if __name__ == "__main__":
    keep_alive()
    twitch_bot = TwitchBot()

    loop = asyncio.get_event_loop()
    loop.create_task(twitch_bot.start())
    loop.create_task(discord_client.start(DISCORD_TOKEN))
    loop.run_forever()

