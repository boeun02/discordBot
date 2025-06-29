import discord
from discord.ext import commands
import asyncio
import webcrawling  # webcrawling 모듈 import
import os
from webcrawling import get_bus_info

intents = discord.Intents.default()
intents.messages = True # 메세지 인텐트 활성화
intents.message_content = True # 메세지 내용 인텐트 활성화
intents.guilds = True # 서버 관련 이벤트 처리를 위해 필요

# 디스코드 클라이언트(봇) 생성
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name}이 연결되었습니다!')

@bot.event
async def on_guild_join(guild):
    # 새로운 채널 생성 및 사용법 안내 메시지 개시
    channel = await guild.create_text_channel('봇 사용법')
    await channel.send(
        "대전대소식 봇 사용법: \n"
        "/대전대소식 - 대전대학교의 공지사항을 검색합니다. \n"
        "사용 방법: "
        "1. /대전대소식 명령어를 입력하고, "
        "봇이 카테고리 선택을 요청하면 학사, 장학, 행사 중 하나를 선택하세요. \n"
        "2. 그 후 검색하고자 하는 키워드를 슬래시(/)와 함께 입력합니다. \n"
        "3. 명령어를 한번 입력하면 봇은 꺼집니다. 한번 더 입력하고싶다면 다시 /대전대소식을 입력한 뒤 선택 항목을 입력해주세요."
    )

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 처리하지 않음
    if message.author == bot.user:
        return

    # '/대전대소식' 명령어 이후의 메시지 처리
    if message.content.startswith('/대전대소식'):
        # 카테고리 선택 메시지를 보냄
        await message.channel.send("카테고리를 선택해주세요: /학사, /장학, /행사")
        return
    
    # '/통학버스' 명령어 이후의 메세지 처리
    if message.content.startswith('/통학버스'):
        # 통학버스 관련 카테고리 선택 메세지를 보냄
        await message.channel.send("통학버스 정보를 선택해주세요: /시간표, /노선")
        return

    # 카테고리 선택 처리
    if message.content.startswith('/'):
        category = message.content.strip('/')
        
        # 대전대 카테고리 처리
        if category in ["학사", "장학", "행사", "컴공"]:
            # 대전대소식 관련 웹크롤링 로직
            if category == "학사":
                mi = '1165'; bbsId = '1861'
            elif category == "장학":
                mi = '3957'; bbsId = '1853'
            elif category == "행사":
                mi = '1191'; bbsId = '1043'
            elif category == "컴공":
                mi = '2241'; bbsId = '1354'

            notice = webcrawling.get_dju_notice_with_category(mi, bbsId, "")
            await message.channel.send(notice or "공지사항을 찾을 수 없습니다.")

        # 통학버스 카테고리 처리
        elif category in ["시간표", "노선", "시내버스"]:
            # 통학버스 관련 웹크롤링 로직
            if category == "시간표":
                cntntsId = '1828'; mi = '2954'
            elif category == "노선":
                cntntsId = '1829'; mi = '2955'
            elif category == "시내버스":
                cntntsId = '1831'; mi = '2957'

            bus_info = get_bus_info(cntntsId, mi)
            await message.channel.send(bus_info or f"{category} 정보를 찾을 수 없습니다.")
        return

# 봇 토큰
bot.run('MTE3ODg1NTczNjYyMTY3MDQzMA.G2Gcao.hWjv8mur5QuJvTVE504vyTRlVO0BU9LdYktXyM')
