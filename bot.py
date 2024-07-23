import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

# intents 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # 메시지 내용을 읽기 위해 추가

bot = commands.Bot(command_prefix="!", intents=intents)

# 메시지를 삭제할 특정 채널 ID
TARGET_CHANNEL_ID = 123456789012345678  # 여기에 삭제할 채널의 ID를 입력하세요.

async def clean_channel(channel):
    # 채널의 모든 메시지 가져오기
    messages = [msg async for msg in channel.history(limit=None)]
    
    if messages:
        latest_message = messages[0]  # 가장 최근 메시지
        for msg in messages:
            if msg.id != latest_message.id:
                try:
                    await msg.delete()
                except discord.Forbidden:
                    print("봇이 메시지를 삭제할 권한이 없습니다.")
                except discord.HTTPException as e:
                    print(f"메시지 삭제 중 오류 발생: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # 봇이 로그인될 때 특정 채널의 메시지 정리
    for guild in bot.guilds:
        channel = guild.get_channel(TARGET_CHANNEL_ID)
        if channel:
            await clean_channel(channel)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == TARGET_CHANNEL_ID:
        async for msg in message.channel.history(limit=None):
            if msg.id != message.id:
                try:
                    await msg.delete()
                except discord.Forbidden:
                    print("봇이 메시지를 삭제할 권한이 없습니다.")
                except discord.HTTPException as e:
                    print(f"메시지 삭제 중 오류 발생: {e}")

    # 다른 명령어 처리와 충돌하지 않도록 on_message를 오버라이드 할 때 필요
    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))
