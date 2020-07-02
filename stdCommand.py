import twitch
import keyboard
import asyncio
import json
import os
import customCommand
import typing

class stdCommandsHandler:
    
    commands: dict = \
    {
        'addCommand': 'add a custom command',
        'cmds': 'display this message',
        'help': 'display the help string of the specified command',
        'cs': 'change symbol for this channel, requires mod powers'
    }
    channel: str
    chat: twitch.Chat

    def __init__(self, channel: object):
        self.channel = channel.channel
        self.chat = channel.chat
        import Channel
        self.channelObj: Channel.Channel = channel

    # commands declarations have this syntax:
    # async def COMMANDNAME (self, variable: str, sender: str )
    # where variable is the command parameter (if there's onne) and is of type str
    # where sender is the username of the user that issued the command and is of type str

    async def help(self, variable: str, sender: str):
        if variable in self.commands.keys():
            self.chat.send(self.commands[variable])
        elif variable in self.channelObj.customCommands.keys():
            try:
                msg: str = self.channelObj.customCommands[variable]['help']
            except Exception:
                chat.send("this command don't have a help string")
            else:
                self.chat.send()
        
    async def addCommand(self, variable: str, sender: str):
        # check if sender is mod
        if self.channelObj.ismod(sender):
            # add a custom command
            await self.channelObj.customCommandhandler.add(variable)
        self.chat.send("you're not a mod!")
        

    async def cmds(self, variable: str, sender: str):
        self.chat.send(f'avaiable commands: addCommand, cmds, help, cs')
    
    async def cs(self, variable: str, sender: str):
        if not self.channelObj.ismod(sender):
            self.chat.send("you're not a mod!")
            return
        variable = variable.strip()
        if len(variable) > 1:
            self.chat.send('the symbol is max 1 character')
            return
        elif variable in ['', ' ']:
            self.chat.send('symbol not valid')
            return
        else:
            self.channelObj.symbol = variable
            self.chat.send(f'symbol has been changed to {variable}')

    async def saveChannelData(self, variable: str, sender: str):
        if not self.channelObj.isop(sender):
            self.chat.send('To perform this action op permissions are required')
            return
		# read last data
        with open('./channels.json', 'r') as file:
            data: dict = json.load(file)
        data[f'#{self.channel}']['moderators'] = self.channelObj.moderators
        data[f'#{self.channel}']['operators'] = self.channelObj.operators
        data[f'#{self.channel}']['customCommands'] = self.channelObj.customCommands
        data[f'#{self.channel}']['symbol'] = self.channelObj.symbol
		# write updated data
        with open('./channels.json', 'w') as file:
            json.dump(data, file, indent=4)

    async def sendChannelData(self, variable: str, sender: str):
        if not self.channelObj.ismod(sender):
            self.chat.send('To perform this action mod permissions are required')
            return
        self.chat.send(
            f'infos for {self.channel}, \
            symbol: {self.channelObj.symbol}, \
            mods: {self.channelObj.moderators}, \
            ops: {self.channelObj.operators}, \
            has other bots: {self.channelObj.hasOtherBots}, \
            custom commands: {str( self.channelObj.customCommands.keys() ).replace("dict_keys", "")}'
        )

    async def evalPi(self, variable: str, sender: str):
        if self.channelObj.isop(sender):
            eval(variable)

    async def mod(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            self.channelObj.moderators.append(variable)
            self.channelObj.log(f'now {variable} is a moderator')
            self.chat.send(f'now {variable} is a moderator')

    async def demod(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            self.channelObj.operators.remove(variable)
            self.channelObj.log(f'now {variable} is no longer a moderator')
            self.chat.send(f'now {variable} is no longer a moderator')

    async def op(self, variable: str, sender: str):
        if self.channelObj.isop(sender):
            self.channelObj.operators.append(variable)
            self.channelObj.log(f'now {variable} is an operator')
            self.chat.send(f'now {variable} is an operator')

    async def deop(self, variable: str, sender: str):
        if self.channelObj.isop(sender): 
            self.channelObj.operators.remove(variable)
            self.channelObj.log(f'now {variable} is no longer an operator')
            self.chat.send(f'now {variable} is no longer an operator')

    