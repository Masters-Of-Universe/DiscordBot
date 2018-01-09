from __future__ import absolute_import
import discord
from discord.ext.commands import Bot
from discord.ext import commands

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DiscordBot(metaclass=Singleton):
	"""Classe définissant un bot discord"""

	def __init__(self):
		self.bot = Bot(description="DiscordBot", command_prefix="!", pm_help = True)
