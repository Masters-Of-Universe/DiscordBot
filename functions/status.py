from __future__ import absolute_import
import asyncio
from aiohttp import ClientSession
import requests
import platform
import json
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import settings
from . import bot
import threading
import time
from io import BytesIO
from PIL import Image
from io import StringIO
from urllib.request import urlopen
import urllib.request
import io
import os
from . import minecraftstatus

CLIENT = bot.DiscordBot().bot

async def joke():
    URL = 'http://explosm.net/rcg'
    explosmResult = str((requests.get(URL).content))
    nb = explosmResult.find(URL)
    text = explosmResult[nb+23:(nb+9+23)]
    embeddisc = discord.Embed(title="Joke", description="http://explosm.net/rcg/" + text, color=0xea7938)
    embeddisc.set_image(url="http://files.explosm.net/rcg/" + text + ".png")
    await CLIENT.say(embed=embeddisc)

async def check_minecraft_status():
    await CLIENT.wait_until_ready()
    options = {
           "red" : red,
           "green" : green,
           "yellow" : yellow,
    }
    sessionclient = ""
    sessionserver = ""
    authclient    = ""
    authserver    = ""
    strpb         = ""
    channel = discord.utils.get(CLIENT.get_all_channels(), name=settings.MINECRAFT_CHANNEL)
    minecraftStatus = await minecraftstatus.MinecraftStatus()
    if (authserver == ""):
        sessionclient = minecraftStatus.sessionclient
        sessionserver = minecraftStatus.sessionserver
        authclient    = minecraftStatus.authclient
        authserver    = minecraftStatus.authserver
    while not CLIENT.is_closed:
        minecraftStatus = await minecraftstatus.MinecraftStatus()
        if (sessionclient != minecraftStatus.sessionclient):
            strpb = ""
            etat, description = options[minecraftStatus.sessionclient]()
            strpb += '''{0} {1} \n'''.format(str(minecraftStatus.sessionclient),str(etat))
            strpb = strpb.replace("green", ":large_blue_circle:").replace("yellow", ":white_circle:").replace("red", ":red_circle:")
            await DisplayEmbed(channel,"Etats des services Minecraft",description,"session.minecraft.net",strpb)
        if (sessionserver != minecraftStatus.sessionserver):
            strpb = ""
            etat, description = options[minecraftStatus.sessionserver]()
            strpb += '''{0} {1} \n'''.format(str(minecraftStatus.sessionserver),str(etat))
            strpb = strpb.replace("green", ":large_blue_circle:").replace("yellow", ":white_circle:").replace("red", ":red_circle:")
            await DisplayEmbed(channel,"Etats des services Minecraft",description,"sessionserver.mojang.com",strpb)
        if (authclient != minecraftStatus.authclient):
            strpb = ""
            etat, description = options[minecraftStatus.authclient]()
            strpb += '''{0} {1} \n'''.format(str(minecraftStatus.authclient),str(etat))
            strpb = strpb.replace("green", ":large_blue_circle:").replace("yellow", ":white_circle:").replace("red", ":red_circle:")
            await DisplayEmbed(channel,"Etats des services Minecraft",description,"auth.mojang.com",strpb)
        if (authserver != minecraftStatus.authserver):
            strpb = ""
            etat, description = options[minecraftStatus.authserver]()
            strpb += '''{0} {1} \n'''.format(str(minecraftStatus.authserver),str(etat))
            strpb = strpb.replace("green", ":large_blue_circle:").replace("yellow", ":white_circle:").replace("red", ":red_circle:")
            await DisplayEmbed(channel,"Etats des services Minecraft",description,"authserver.mojang.com",strpb)
        sessionclient = minecraftStatus.sessionclient
        sessionserver = minecraftStatus.sessionserver
        authclient    = minecraftStatus.authclient
        authserver    = minecraftStatus.authserver
        strpb = ""
        await asyncio.sleep(300)

def red():
    return ("Offline","Stopped service.")

def green():
    return ("Online","Online service")

def yellow():
    return ("Warning","Slow service.")

async def DisplayEmbed(channel,title,description,name,value):
    embeddisc = discord.Embed(title=title, description=description, color=0xea7938)
    embeddisc.add_field(name=name,value=value,inline=False)
    await CLIENT.send_message(channel,embed=embeddisc)

async def server(url):
    servdesc = ""
    channel = discord.utils.get(CLIENT.get_all_channels(), name=settings.MINECRAFT_CHANNEL)
    server = channel.server

    async with ClientSession() as session:

        async with session.get(url) as response:
            response = await response.read()
            rcronResult = json.loads(response)

            online = rcronResult['online']
            host = rcronResult['hostname']
            status = rcronResult["status"]

            if (online == 1):
                servdesc = rcronResult['motd']
                port = rcronResult['port']
                version = rcronResult['minecraftVersion']
                nbjoueuronline = rcronResult['player']
                players = rcronResult['players']
                nbmax = rcronResult['maxPlayer']
                strplayer = ""
                listemoji = []
                listenameemoji = []

                for emoji in server.emojis:
                    listemoji.append(emoji)
                    listenameemoji.append(emoji.name)

                await CLIENT.change_presence(game=discord.Game(name="",type=0))
                await CLIENT.change_presence(game=discord.Game(name="Minecraft", type=0))

                embeddisc = discord.Embed(title=host, description=servdesc, color=0xea7938)
                embeddisc.set_thumbnail(url=settings.SERV_IMAGE)
                embeddisc.add_field(name="Version",value=version,inline=False)
                embeddisc.add_field(name="Status",value=":large_blue_circle: Online",inline=True)

                embeddisc.add_field(name="Ping",value=":ping_pong: " +  str("100") + " ms",inline=True)
                for player in players:
                    async with session.get("https://api.mojang.com/users/profiles/minecraft/" + player) as minecraftskin:
                        minecraftskin = await minecraftskin.read()
                        apiMojangResult = json.loads(minecraftskin)
                        urllib.request.urlretrieve("https://crafatar.com/renders/head/" + apiMojangResult['id'], str(player) + ".png")
                        with open(str(player) + ".png", "rb") as image:
                            if (str(player) not in listenameemoji):
                                emoji = await CLIENT.create_custom_emoji(server, name=str(player), image=image.read())
                            else:
                                emoji = listemoji[listenameemoji.index(str(player))]

                        strplayer += '''• {0} {1} \n'''.format(str(emoji), str(player))

                embeddisc.add_field(name="Players ({0}/{1})".format(str(nbjoueuronline),str(nbmax)),value=strplayer, inline=False)
                await CLIENT.edit_channel(channel, topic="The server is ONLINE [" + str(nbjoueuronline) + "/" + str(nbmax) + " players] (" + str("100") + " ms)")
            else:
                embeddisc = discord.Embed(title=host, description=":red_circle: " + status, color=0xea7938)
                embeddisc.set_thumbnail(url=settings.SERV_IMAGE)
                
                await CLIENT.edit_channel(channel, topic="The server is OFFLINE.")

            await CLIENT.say(embed=embeddisc)
