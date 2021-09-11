#Auto Loop
# -*- coding: utf-8 -*-
import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
import lxml
import datetime
import asyncio
import discord
import logging
import random
import math
import functools
import itertools
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
import youtube_dl.utils
import city
import urllib.parse, urllib.request, re
from gtts import gTTS #tts 기능
import ffmpeg
import openpyxl
import sys
import urllib.request
import json
from datetime import datetime
import time
from matplotlib import pyplot as plt
import os
import wmi
import psutil
import platform
from datetime import datetime
import time
import cpuinfo
import traceback
import dbkrpy


bot = commands.Bot(command_prefix = '-')

DBKR_token = ""
token = '' 
dbkrpy.UpdateGuild(bot,DBKR_token)

@bot.remove_command('help')



@bot.event
async def on_ready():
    print("I'm ready") 
    game = discord.Game(".도움말 | {}개의 서버에 가입되어 있습니다.".format(str(len(bot.guilds))))
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)
@bot.command('날씨')
async def weather_output(context, city):
    api_address = "http://api.weatherstack.com/current?access_key=96b61cb41acaad6fe3b5d8b31465a586&query="
    api_url = api_address + city
    json_data = requests.get(api_url).json()

    city_name = json_data["location"]["name"]
    temperature = json_data["current"]["temperature"]
    weather_description = json_data["current"]["weather_descriptions"][0]

    embed=discord.Embed(title="날씨 정보", description="날씨정보를 보여줍니다.", color=0x00ffff)
    embed.add_field(name=(f'\n도시: {city_name} \n온도는 {temperature} 입니다. \n날씨는 {weather_description}'), value=("아직 영어밖에 안됩니다."), inline=False)
    await context.send(embed=embed)

@bot.command('코로나')
async def corona(ctx):
    address = "http://ncov.mohw.go.kr"

    response = requests.get(address)
    soup = BeautifulSoup(response.text,'lxml')
    확진자 = soup.select('div.liveboard_layout div.liveNum span.num')
    await ctx.send('``차례대로 확진환자, 완치, 치료 중, 사망 순입니다.``')
    for b in 확진자:
        await ctx.send('``'+b.text+'명``')

@bot.command('현재시각')
async def now_time(ctx):
    datetime_object = datetime.datetime.now()
    await ctx.send(f'``현재 시각은 {datetime_object} 입니다.``')

@bot.command()
async def api핑(ctx):
    latency = bot.latency
    await ctx.send(f'현재핑은 ``{round(latency * 1000)}``ms 입니다.')

@bot.command('따라해')
async def echo(ctx, *, content: str):
    await ctx.send(content)

# @bot.event
# async def on_command_error(ctx: commands.Context, error: Exception):
#     if isinstance(error, (commands.CommandNotFound)):
        

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    try: 
        if isinstance(error, (commands.CommandNotFound)):
            userid = ctx.message.author.id
            channel = ctx.author.voice.channel
            language = 'ko'
            output = gTTS(text="제가 잘이해한건지 모르겠네요.",lang=language,slow=False)
            output.save("idk.mp3")
            #if not connected
            if ctx.voice_client is None:
                vc = await channel.connect()
                await ctx.send(f'<@!{userid}> 제가 잘이해한건지 모르겠네요.')
                vc.play(discord.FFmpegPCMAudio('idk.mp3'))
                return
            else:
                await ctx.send(f'<@!{userid}> 제가 잘이해한건지 모르겠네요.')
                ctx.voice_client.play(discord.FFmpegPCMAudio('idk.mp3'))
                return
    except :
        userid = ctx.message.author.id
        await ctx.send(f"<@!{userid}> 제가 잘이해한건지 모르겠네요.")

@bot.command()
async def 유저정보(ctx, member: discord.Member):
    embed=discord.Embed(title="유저 정보", description="유저정보를 불러옵니다.", color=0x00ffff)
    embed.add_field(name=("멍청한 먼지가 만들었습니다."), value=(f'유저 이름: {member.name}, 아이디: {member.id}'), inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def 내정보(ctx):
    member = ctx.message.author
    embed=discord.Embed(title="유저 정보", description="유저정보를 불러옵니다.", color=0x00ffff)
    embed.add_field(name=("멍청한 먼지가 만들었습니다."), value=(f'유저 이름: {member.name}, 아이디: {member.id}'), inline=True)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def 주사위(ctx):
    dice = random.randint(1, 6)
    if dice == 1:
        await ctx.send("1이 나왔습니다.")
    if dice == 2:
        await ctx.send("2가 나왔습니다.")
    if dice == 3:
        await ctx.send("3가 나왔습니다.")
    if dice == 4:
        await ctx.send("4가 나왔습니다.")
    if dice == 5:
        await ctx.send("5가 나왔습니다.")    
    if dice == 6:
        await ctx.send("6이 나왔습니다.")


    
    
async def text2Speech(language,text,ctx,channel):
    myText = text
    language = language
    output = gTTS(text=myText,lang=language,slow=False)
    output.save("output.mp3")
    #if not connected
    if ctx.voice_client is None:
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio('output.mp3'))
    else:
        ctx.voice_client.play(discord.FFmpegPCMAudio('output.mp3'))



@bot.command()
async def tts접속(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def tts접속해제(ctx):
    await ctx.voice_client.disconnect()

@bot.command(name='음성말해')
async def t2s(ctx,*argv):
    channel = ctx.author.voice.channel
    text = ""
    for i in range(1,len(argv)):
        text += argv[i]
    language = argv[0]
    await text2Speech(language,text,ctx,channel)
    #await ctx.send("Lang is {} and the sentence is:  {} ".format(arg1,arg2)


@bot.command()
async def 가위(ctx):
    str1 = ['가위','바위','보']
    r=random.choice(str1)
    if r == '가위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✌️ vs ✌️ 비겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '바위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✌️ vs 👊 당신이 졌습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '보':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✌️ vs ✋ 당신이 이겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)

@bot.command()
async def 바위(ctx):
    str1 = ['가위','바위','보']
    r=random.choice(str1)
    if r == '가위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n👊 vs ✌️ 당신이 이겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '바위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n👊 vs 👊 비겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '보':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n👊 vs ✋ 당신이 졌습니다.", color=0x00ffff)
        await ctx.send(embed=embed)

@bot.command()
async def 보(ctx):
    str1 = ['가위','바위','보']
    r=random.choice(str1)
    if r == '가위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✋ vs ✌️ 당신이 졌습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '바위':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✋ vs 👊당신이 이겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)
    elif r == '보':
        embed = discord.Embed(title="가위 바위 보", description= r + "\n✋ vs ✋비겼습니다.", color=0x00ffff)
        await ctx.send(embed=embed)


bot.run(token) 
