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

CLIENT = bot.DiscordBot().bot

async def server(url):
	servdesc = ""
	channel = discord.utils.get(CLIENT.get_all_channels(), name='test-bot')
	async with ClientSession() as session:
		async with session.get(url) as response:
			response = await response.read()
			d = json.loads(response)

			online = d['online']
			host = d['hostname']
			status = d["status"]

			if ((online) == 1):
				servdesc = d['motd']
				port = d['port']
				version = d['minecraftVersion']
				nbjoueuronline = d['player']
				players = d['players']
				nbmax = d['maxPlayer']
				strplayer = ""
				embeddisc = discord.Embed(title=host, description=servdesc, color=0xea7938)
				embeddisc.add_field(name="Version",value=version,inline=False)
				embeddisc.add_field(name="Status",value=":large_blue_circle: Online",inline=True)
				async with session.get("https://minecraft-api.com/api/ping/ping.php?ip=" + str(host) + "&port=" + str(port)) as ping:
					leping = await ping.text()
					leping = float(leping) * 10000
					embeddisc.add_field(name="Ping",value=":ping_pong: " +  str(leping) + " ms",inline=True)
				embeddisc.add_field(name="Players",value=":video_game: " + str(nbjoueuronline) + "/" + str(nbmax),inline=True)
				for player in players:
					strplayer += ", " + player

				embeddisc.add_field(name="Players",value=strplayer[2:], inline=False)
				await CLIENT.edit_channel(channel, topic="The server is ONLINE [" + str(nbjoueuronline) + "/" + str(nbmax) + " players] (" + str(leping) + " ms)")
			else:
				embeddisc = discord.Embed(title=host, description=":red_circle: " + status, color=0xea7938)
				await CLIENT.edit_channel(channel, topic="The server is OFFLINE.")
			
			await CLIENT.say(embed=embeddisc)
