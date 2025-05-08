# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:54:35 2025

@author: User
"""

import discord
import time
from twitchio import Client, Message
import asyncio
from dotenv import load_dotenv
import os

# 讀取 .env 配置
load_dotenv()

# Discord bot 設定
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')  # 伺服器 ID
CHANNEL_ID = os.getenv('CHANNEL_ID')  # 頻道 ID

# 初始化 Discord 客戶端
discord_client = discord.Client()

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')

# 發送訊息到 Discord 頻道
async def send_to_discord(message):
    channel = discord_client.get_channel(int(CHANNEL_ID))
    await channel.send(message)

# Twitch bot 設定
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
TWITCH_NICK = os.getenv('TWITCH_NICK')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')

class TwitchBot(Client):
    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, nick=TWITCH_NICK)

    async def event_ready(self):
        print(f'Logged in as {self.nick}')
        channel = await self.join_channels([TWITCH_CHANNEL])
        print(f'Joined channel: {channel.name}')

    async def event_message(self, message: Message):
        if message.author.name.lower() != TWITCH_NICK.lower():
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            log_message = f'[{timestamp}] {message.author.name}: {message.content}'

            # 把訊息紀錄到 Discord
            await send_to_discord(log_message)

            # 可以選擇將訊息記錄在本地的 .txt 檔案
            with open(f'logs/{message.author.name}.txt', 'a') as f:
                f.write(log_message + '\n')

# 啟動 Discord bot 和 Twitch bot
async def start_bots():
    twitch_bot = TwitchBot()
    discord_thread = asyncio.create_task(discord_client.start(DISCORD_TOKEN))
    twitch_thread = asyncio.create_task(twitch_bot.start())
    await asyncio.gather(discord_thread, twitch_thread)

# 執行程式
if __name__ == "__main__":
    asyncio.run(start_bots())
