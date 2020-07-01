import twitch
import keyboard
import asyncio
import json
import os
import customCommand
import typing
import stdCommand


class Channel:

    symbol = '!'
    channel: str
    operators: list
    moderators: list
    commandHandlers: list
    customCommands: dict
    customCommandhandler: customCommand.customCommandsHandler
    stdCommandHandler: stdCommand.stdCommandsHandler
    chat: twitch.Chat = None

    def __init__(self, channel: str):
        self.channel = channel.lower()
        self.chat = twitch.Chat(
            channel=self.channel,
            nickname=os.getenv('USERNAME'),
            oauth=os.getenv('OAUTH_TOKEN')
        )
        with open('channels.json', 'r') as file:
            channelData = json.load(file)[f'#{self.channel}']
        self.symbol = channelData['symbol']
        self.operators = channelData['operators']
        self.moderators = channelData['moderators']
        self.customCommands = channelData['customCommands']
        self.customCommandhandler = customCommand.customCommandsHandler()
        self.customCommandhandler.addChannelObj(self)
        self.customCommandhandler.channel = self.channel
        self.customCommandhandler.chat = self.chat
        self.chat.subscribe(self.preCommandHandler)

    # handler is a function that recives a message object
    def onMessage(self, handler) -> None:
        self.chat.subscribe(handler)
    
    # handler is a function that recives 3 str, command, variable, sender
    def onCommand(self, handler) -> None:
        self.commandHandlers.append(handler)

    # preprocess the message before executing the handlers/callbacks
    def preCommandHandler(self, message: twitch.chat.message) -> None:
        # if the message doesn't start with SYMBOL is not a command
        if not message.text.startswith(self.symbol): return
        # remove the SYMBOL
        text = message.text.replace(self.symbol, '', 1)
        # if there's a variable, take it
        try:
            command, variable = text.split(' ', 1)
        except:
            command, variable = text, None
        # if there's a @ has a mentions
        hasPing = '@' in str(variable)
        # is a custom command?
        isCustom = command in self.customCommands
        # print command infos
        self.log(f'command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {isCustom}')
        # if the stdCommandHandler has this method, you that method
        if hasattr( self.stdCommandHandler, command ):
            # its kinda a mess, but it should do the work
            #				stdCommandHandler		get cmd method			execute with parameters
            asyncio.run( self.stdCommandHandler.__getattribute__(command)( variable, message.sender ) )
		# else if is a custom command
        elif isCustom is True:
			# execute with custom commands parser
			#				customCommandHandler	execute "command" with parameters
            asyncio.run( self.customCommandhandler.execute( command, variable, message.sender ) )
		# if nothing worked, send the command to the registered "other" handlers
        else:
			# cicle in all registered handlers
            for handler in self.commandHandlers:
				# try to execute them
                try:
                    asyncio.run( handler( command, variable, message.sender ) )
				# if the handler isn't a coroutine, skip it
                except Exception as e:
					# log the error
                    self.log(f'error! {e}')
                    continue
	
	# a small function that "pretty prints" messages
    def log(self, txt: str) -> None:
        print(f'{self.channel} - {txt}')

	# before deleting the object save all its data
    def __del__(self):
		# read last data
        with open('./channels.json', 'r') as file:
            data: dict = json.load(file)
        data[f'#{self.channel}']['moderators'] = self.moderators
        data[f'#{self.channel}']['operators'] = self.operators
        data[f'#{self.channel}']['customCommands'] = self.customCommands
        data[f'#{self.channel}']['symbol'] = self.symbol
		# write updated data
        with open('./channels.json', 'w') as file:
            json.dump(data, file, indent=4)


