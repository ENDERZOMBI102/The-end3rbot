import sys
from os import getenv
from typing import List
import json
import importlib

import twitchio.dataclasses
from twitchio.ext import commands

import TwitchBotV2.Channel


class Client(commands.Bot):

	channels: List[ TwitchBotV2.Channel.Channel ] = []

	def __init__(self):
		super().__init__(
			client_id=getenv('TWITCH_CLIENT_ID'),
			irc_token=getenv('TWITCH_OAUTH_TOKEN'),
			nick=getenv('TWITCH_USERNAME'),
			prefix='!',
			initial_channels=['ENDERZOMBI102']
		)
		self.loadChannels()

	async def event_pubsub(self, data):
		pass

	# Events don't need decorators when subclassed
	async def event_ready(self):
		print(f'TwitchBotV2 Ready | {self.nick}')

	async def event_message(self, msg: twitchio.Message):
		if msg.content == '!reload channel':
			await msg.channel.send('reloading!')
			print('reload issued!')
			importlib.reload( sys.modules[ TwitchBotV2.Channel.__module__ ] )
			self.loadChannels()
			await msg.channel.send('reloaded!')
		else:
			for channel in self.channels:
				if channel.name == msg.channel.name:
					await channel.preCommandHandler( msg )
					break

	def loadChannels(self):
		with open('./channels.json', 'r') as file:
			data = json.load(file)
		for channel in data:
			self.channels.append( TwitchBotV2.Channel( channel ) )
		if len( self.channels ) == 0:
			self.channels.append( TwitchBotV2.Channel.create( 'enderzombi102' ) )
