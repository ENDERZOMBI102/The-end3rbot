import twitch
import keyboard
import asyncio
import json
import os
import TwitchBot.customCommand as customCommand
import typing
from pathlib import Path
import TwitchBot.stdCommand as stdCommand


def createDictFromTemplate(channel: str) -> dict:
        channel = channel.lower()
        if '#' in channel:
            channel = channel.replace('#','')
        return {
            f'#{channel}' : {
                'symbol' : '!',
                'hasOtherBots' : False,
                'moderators' : [
                    
                ],
                'operators'  : [
                    channel
                ],
                'customCommands' : {

                }
            }
        }

class Channel:

    symbol: str
    channel: str
    operators: list
    moderators: list
    commandHandlers: list = []
    customCommands: dict
    customCommandhandler: customCommand.customCommandsHandler
    stdCommandHandler: stdCommand.stdCommandsHandler
    hasOtherBots: bool
    chat: twitch.Chat

    def __init__(self, channel: str):
        self.channel = channel.lower()
        self.chat = twitch.Chat(
            channel=self.channel,
            nickname=os.getenv('TWITCH_USERNAME'),
            oauth=os.getenv('TWITCH_OAUTH_TOKEN')
        )
        if not Path('./channels.json').exists():
            with open('channels.json', 'x') as file:
                    json.dump( createDictFromTemplate(self.channel) )
        else:
            data: dict = None
            try:
                with open('channels.json', 'r') as file:
                    data = json.load(file)
                    channelData = data[f'#{self.channel}']
            except Exception:
                channelData = createDictFromTemplate(self.channel)[f'#{self.channel}']
                data[f'#{self.channel}'] = channelData
                with open('channels.json', 'w') as file:
                    json.dump(data, file, indent=4)

        self.symbol = channelData['symbol']
        self.operators = channelData['operators']
        self.moderators = channelData['moderators']
        self.hasOtherBots = channelData['hasOtherBots']
        self.customCommands = channelData['customCommands']
        self.stdCommandHandler = stdCommand.stdCommandsHandler(self)
        self.customCommandhandler = customCommand.customCommandsHandler()
        self.customCommandhandler.addChannelObj(self)
        self.customCommandhandler.channel = self.channel
        self.customCommandhandler.chat = self.chat
        self.chat.subscribe(self.preCommandHandler)
        self.chat.send('The end3rbot successfully connected')
        self.log('ready')

    # handler is a function that recives a message object
    def onMessage(self, handler: typing.Callable) -> None:
        self.chat.subscribe(handler)
    
    # handler is a function that recives 3 str, command, variable, sender
    def onCommand(self, handler: typing.Callable) -> None:
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
            command, variable = text, ''
        # if there's a @ has a mentions
        hasPing = '@' in str(variable)
        # is a custom command?
        isCustom = command in self.customCommands
        # log command infos
        self.log(f'command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {isCustom}, sender: {message.sender}')
        # if the stdCommandHandler has this method, you that method
        if hasattr( self.stdCommandHandler, command ):
            # its kinda a mess, but it should do the work
            #				        stdCommandHandler	get method			execute with parameters
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
        elif isCustom is True:
			# execute with custom commands parser
			#				customCommandHandler	execute "command" with parameters
            asyncio.run( self.customCommandhandler.execute( command, variable, message.sender ) )
		# if nothing worked, send the command to the registered "other" handlers
        else:
            handled: bool = False
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
                else:
                    #command was ipotetically handled
                    handled = True
            if not ( handled is True ) or ( self.hasOtherBots is True ):
                self.log(f'unknown command: {command}')
                self.chat.send(f'unknown command: {command}')
	# a small function that "pretty prints" messages
    def log(self, txt: str):
        print(f'{self.channel} - {txt}')

    # return true if user is op
    def isop(self, user: str):
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

	# before deleting the object save all its data
    def __del__(self):
		# mode '+' makes so we can read and write
        with open( './channels.json', mode='r' ) as file:
            # read last data
            data: dict = json.load(file)
            # update data
            data[f'#{self.channel}']['moderators'] = self.moderators
            data[f'#{self.channel}']['operators'] = self.operators
            data[f'#{self.channel}']['customCommands'] = self.customCommands
            data[f'#{self.channel}']['hasOtherBots'] = self.hasOtherBots
            data[f'#{self.channel}']['symbol'] = self.symbol
        with open('./channels.json', 'w') as file:
            # write updated data
            json.dump(data, file, indent=4)

