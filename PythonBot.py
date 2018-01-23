import functions
from functions import status, bot, permissions
import threading
import settings
import time
import discord
import asyncio

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

@CLIENT.command(pass_context=True)
async def online(ctx,*args):
	base_url = settings.API_HOST + "status/online"
	await status.server(base_url)

@CLIENT.command(pass_context=True)
async def offline(ctx,*args):
	base_url = settings.API_HOST + "status/offline"
	await status.server(base_url)

@CLIENT.command(pass_context=True)
async def joke(ctx,*args):
	await status.joke()

@CLIENT.command(pass_context=True)
async def moubot(ctx,*args):
	await status.moubot()

@CLIENT.command(pass_context=True)
async def mc(ctx,*args):
        """Display the help menu for the minecraft server"""
        if ctx.message.channel.name == "test-bot":
            embed = discord.Embed(title="Minecraft commands", colour=discord.Colour(0xdc4643))
            embed.set_thumbnail(
                url=settings.SERV_IMAGE)
            embed.set_author(
                name="MouBot", icon_url=settings.AUTHOR_IMAGE)
            embed.set_footer(
                text="MouBot", icon_url=settings.FOOTER_IMAGE)
            embed.add_field(name=".help mc", value="Displays this help menu.\n")
            embed.add_field(name=".status", value="Displays the current server status.\n")
            embed.add_field(name=".info", value="Information about how to connect to server.\n")
            await CLIENT.say(embed=embed)

@CLIENT.command(pass_context=True)
async def clear(ctx,count=10):
	if (permissions.isAdmin(ctx.message.author)):
		number = int(count)
		count = 0
		if number <= 100:
			async for x in CLIENT.logs_from(ctx.message.channel, limit = number):
				count += 1
				await CLIENT.delete_message(x)
		lastmess = await CLIENT.say("You have deleted `{0} messages`.".format(str(count)))
		await asyncio.sleep(2)
		await CLIENT.delete_message(lastmess)

CLIENT.loop.create_task(status.check_minecraft_status())
CLIENT.run(settings.TOKEN_BOT)
