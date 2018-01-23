from __future__ import absolute_import
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from aiohttp import ClientSession
import requests
import platform
import json
from asyncinit import asyncinit

@asyncinit
class MinecraftStatus:

    """Constructeur de notre classe"""
    async def __init__(self):
        async with ClientSession() as session:
        	async with session.get("https://status.mojang.com/check") as checkstatus:
        		minecraftcheck = await checkstatus.read()
        		mojangApiResult = json.loads(minecraftcheck)
        		self.sessionclient = mojangApiResult[1]['session.minecraft.net']
        		self.sessionserver = mojangApiResult[6]['sessionserver.mojang.com']
        		self.authclient    = mojangApiResult[3]['auth.mojang.com']
        		self.authserver	   = mojangApiResult[5]['authserver.mojang.com']
