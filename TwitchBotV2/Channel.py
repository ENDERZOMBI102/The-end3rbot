from os import getenv
from typing import List
import json
import asyncio

import twitchio.dataclasses

import TwitchBotV2.customCommand as customCommand
import TwitchBot.stdCommand as stdCommand


class Channel:

    # data
	channel: str
	hasOtherBots: bool
	prefix: str
	moderators: List[str]
	operators: List[str]
	client: twitchio.Client
	chat: twitchio.dataclasses.Channel
	customCommandHandler: customCommand
	stdCommands: stdCommand

	def __init__(self, channelData: dict):
		self.channel = channelData['channel']
		self.hasOtherBots = channelData['hasOtherBots']
		self.prefix = channelData['prefix']
		self.moderators = channelData['moderagors']
		self.operators = channelData['operators']
		self.client = twitchio.Client( client_id=getenv('TWITCH_CLIENT_ID') )
		self.chat = twitchio.dataclasses.Channel(channel)
		self.customCommandHandler = customCommand.customCommandsHandler( self.chat, channelData['commands'] )
		self.stdCommands = stdCommand()

    # preprocess the message before executing the handlers/callbacks
	def preCommandHandler(self, message: twitch.chat.message) -> None:
		# if the message doesn't start with our prefix is not a command
		if not message.text.startswith(self.prefix): return
		# remove the SYMBOL
		text = message.text.replace(self.prefix, '', 1)
		# if there's a variable, take it
		try:
			command, variable = text.split(' ', 1)
		except:
			command, variable = text, ''
		# if there's a @ has a mentions
		hasPing = '@' in str(variable)
		# is a custom command?
		isCustom = command in self.customCommands
		# log command infos
		self.log(
			f'command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {isCustom}, sender: {message.sender}')
		# if the stdCommandHandler has this method, you that method
		if hasattr(self.stdCommandHandler, command):
			# its kinda a mess, but it should do the work
			# 				        stdCommandHandler	get method			execute with parameters
			asyncio.run(
				getattr(
					self.stdCommandHandler,  # object to retrive the method from
					command  # method name
				)(  # calls the method with those as parameter
					variable,
					message.sender
				)
			)  # run the async method
		# else if is a custom command
		elif isCustom:
			# execute with custom commands parser
			asyncio.run( self.customCommandhandler.execute( command, variable, message.sender ) )
        # if the command was not handled print an error message unless the channel has other bots,
        # in that case the other bots may have handled the command
		else:
			self.log(f'unknown command: {command}')
			if not self.hasOtherBots:
				self.chat.send(f'unknown command: {command}')

	# a small function that "pretty prints" messages
	def log(self, txt: str):
		print(f'{self.channel} - {txt}')

	# return true if user is op
	def isop(self, user: str):
		if user == 'SYSTEM' or 'system':
			return True
		try:
			self.operators.index(user)
		except ValueError:
			return False
		else:
			return True

	# return true if user is op
	def ismod(self, user: str):
		try:
			self.moderators.index(user)
		except ValueError:
			return False or self.isop(user)
		else:
			return True

	def __dict__(self):
		return {
            'channel': self.channel,
            'hasOtherBots': self.hasOtherBots,
            'prefix': self.prefix,
            'moderators': self.moderators,
            'operators': self.operators,
            'commands': self.customCommandHandler.commands
        }

	def __del__(self):
		with open('./../channels.json', 'r') as file:
			data = json.load(file)
		for i in range( len(data) ):
			if data[i]['channel'] == self.channel:
				data[i] = self.__dict__
        with open('./../channels.json', 'w') as file:
            data = json.dump(file)
        
	@staticmethod
	def create(channelName: str) -> Channel:
		import TwitchBotV2.utils as utils
		return Channel( utils.createChannelDict( channelName ) )



