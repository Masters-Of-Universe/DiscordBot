import functions
from functions import status, bot
import threading
import settings
import time

CLIENT = bot.DiscordBot().bot

@CLIENT.event
async def on_ready():
	print('Logged in as '+CLIENT.user.name+' (ID:'+CLIENT.user.id+') | Connected to '+str(len(CLIENT.servers))+' servers | Connected to '+str(len(set(CLIENT.get_all_members())))+' users')
	print('--------')
	print('Use this link to invite {}:'.format(CLIENT.user.name))
	print('https://discordapp.com/oauth2/authorize?CLIENT_id={}&scope=bot&permissions=93264'.format(CLIENT.user.id))
	print('--------')

@CLIENT.command(pass_context=True)
async def ping(ctx):
	await CLIENT.say(":ping_pong: Pong!")

@CLIENT.command()
async def online(*args):
	base_url = settings.API_HOST + "status/online"
	await status.server(base_url)

@CLIENT.command()
async def offline(*args):
	base_url = settings.API_HOST + "status/offline"
	await status.server(base_url)

CLIENT.run(settings.TOKEN_BOT)
