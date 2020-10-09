import json

import twitchio

import TwitchBotV2.stdCommand
import TwitchBotV2.customCommand
import TwitchBotV2.utils


class Channel:

	poetMode = False
	disabled = False
	channel: twitchio.Channel = None

	def __init__(self, channelData: dict):
		self.name = channelData['channel']
		self.hasOtherBots = channelData['hasOtherBots']
		self.prefix = channelData['prefix']
		self.operators = channelData['operators']
		self.customCommandHandler = TwitchBotV2.customCommand.customCommandsHandler( self, channelData['commands'] )
		self.stdCommands = TwitchBotV2.stdCommand.stdCommandsHandler( self )

	# preprocess the message before executing the handlers/callbacks
	async def preCommandHandler(self, msg: twitchio.Message) -> None:
		if self.disabled:
			return
		if self.channel is None:
			self.channel = msg.channel
		# if the message doesn't start with our prefix is not a command
		if not msg.content.startswith(self.prefix):
			return
		# remove the prefix
		text = msg.content.replace(self.prefix, '', 1)
		# if there's a variable, take it
		splittedMessage = text.split(' ')
		command = splittedMessage[0]
		try:
			variables = splittedMessage[ 1:len( splittedMessage ) ]
		except ValueError:
			variables = []
		# if there's a @ has a mentions
		hasPing = '@' in str(variables)
		# is a custom command?
		isCustom = command in self.customCommandHandler.commands
		# log command infos
		self.log(
			f'command: {command}, variables: {variables}, has ping: {hasPing}, is custom: {isCustom}, author: {msg.author.name}'
		)
		# if the stdCommandHandler has this method, you that method
		if hasattr(self.stdCommands, command):
			# get the command and execute it
			await getattr(
					self.stdCommands,  # object to retrieve the method from
					command  # method name
				)(  # calls the method with those as parameter
					variables,
					msg
				)  # run the async method
		# else if is a custom command
		elif isCustom:
			# execute with custom commands parser
			await self.customCommandHandler.execute(command, variables, msg)
		# if the command was not handled print an error message unless the channel has other bots,
		# in that case the other bots may have handled the command
		else:
			self.log(f'unknown command: {command}')
			if not self.hasOtherBots:
				await msg.channel.send(f'unknown command: {command}')

	# a small function that "pretty prints" messages
	def log(self, txt: str):
		print(f'{self.name} - {txt}')

	# return true if user is op
	def isop(self, user: str):
		if user.lower() in ['system', self.name]:
			return True
		try:
			self.operators.index(user)
		except ValueError:
			return False
		else:
			return True

	# return true if user is op
	def ismod(self, user: twitchio.User):
		return user.is_mod or self.isop(user.name)

	def save(self):
		# read old data
		with open('./channels.json', 'r') as file:
			data = json.load(file)
		# overwrite our data
		if len(data) != 0:
			for i in range(len(data)):
				if data[i]['channel'] == self.name:
					data[i] = self.__dict__()
		else:
			data.append( self.__dict__() )
		# save new data
		with open('./channels.json', 'w') as file:
			json.dump(data, file, indent=4)

	def __dict__(self):
		return {
			'channel': self.name,
			'hasOtherBots': self.hasOtherBots,
			'prefix': self.prefix,
			'operators': self.operators,
			'commands': self.customCommandHandler.commands
		}

	def __del__(self):
		# read old data
		with open('./../channels.json', 'r') as file:
			data = json.load(file)
		# overwrite our data
		for i in range(len(data)):
			if data[i]['channel'] == self.channel:
				data[i] = self.__dict__
		# save new data
		with open('./../channels.json', 'w') as file:
			json.dump(data, file)

	@staticmethod
	def create(channelName: str) -> object:
		return Channel( TwitchBotV2.utils.createChannelDict( channelName ) )
