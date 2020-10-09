import twitch
import keyboard
import asyncio
import json
import os
import TwitchBotV2.customCommand as customCommand
import typing

class stdCommandsHandler:
    
    commands: dict = \
    {
        'help': 'display the help string of the specified command',
        'addCommand': 'add a custom command, requires mod powers',
        'cmds': 'display this message',
        'cs': 'change symbol for this channel, requires mod powers',
        'saveChannelData': 'saves channel data to disk, requires op powers',
        'sendChannelData': 'send channel data to chat, requires mod powers',
        'evalPi': 'evaluate a py expression, requires op powers',
        'mod': 'makes the given user a mod, requires mod powers',
        'demod':'makes the given user no loger an mod, requires mod powers',
        'op':'makes the given user an op, requires op powers',
        'deop':'makes the given user no loger an op, requires op powers',
        'echo':'echo echo echo',
    }

    channel: str
    chat: twitch.Chat

    def __init__(self, channel: object):
        self.channel = channel.channel
        self.chat = channel.chat
        import TwitchBotV2.Channel as Channel
        self.channelObj: Channel.Channel = channel

    # commands declarations have this syntax:
    # async def COMMANDNAME (self, variable: str, sender: str )
    # where variable is the command parameter (if there's onne) and is of type str
    # where sender is the username of the user that issued the command and is of type str

    async def help(self, variable: str, sender: str):
        if variable == '':
            self.chat.send("ERROR: parameter can't be empty")
        elif variable in self.commands.keys():
            self.chat.send(self.commands[variable])
        elif variable in self.channelObj.customCommands.keys():
            try:
                msg: str = self.channelObj.customCommands[variable]['help']
            except Exception:
                chat.send("this command doesn't have a help string")
            else:
                self.chat.send(msg)
        
    async def addCommand(self, variable: str, sender: str):
        # check if sender is mod
        if self.channelObj.ismod(sender) is True:
            # add a custom command
            await self.channelObj.customCommandhandler.add(variable)
            with open('./../channels.json', 'r') as file:
                data = json.load(file)
            data[f'#{self.channel}']['customCommand'] = self.channelObj.customCommands
            with open('./../channels.json')
                json.dump(data, file, indent=4)
        else:
            self.chat.send('To perform this action mod permissions are required')
        

    async def cmds(self, variable: str, sender: str):
        self.chat.send(
            f'avaiable commands: help, addCommand, cmds, cp, \
            saveChannelData, sendChannelData, evalPi, (de)mod, \
            (de)op'
        )
    
    async def cp(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            variable = variable.strip()
            if len(variable) > 1:
                self.chat.send('the prefix is max 1 character')
                return
            elif variable in ['', ' ']:
                self.chat.send('prefix not valid')
                return
            else:
                self.channelObj.prefix = variable
                self.chat.send(f'prefix has been changed to {variable}')
        else:
            self.chat.send('To perform this action mod permissions are required')

    async def saveChannelData(self, variable: str, sender: str):
        if self.channelObj.isop(sender):
            with open('./channels.json', '+') as file:
                # read last data
                data: dict = json.load(file)
                # update with last data
                data[f'#{self.channel}']['moderators'] = self.channelObj.moderators
                data[f'#{self.channel}']['operators'] = self.channelObj.operators
                data[f'#{self.channel}']['customCommands'] = self.channelObj.customCommands
                data[f'#{self.channel}']['symbol'] = self.channelObj.symbol
                # write updated data
                json.dump(data, file, indent=4)
        else:
            self.chat.send('To perform this action op permissions are required')

    async def sendChannelData(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            self.chat.send(
                f'infos for {self.channel}, \
                symbol: {self.channelObj.symbol}, \
                mods: {self.channelObj.moderators}, \
                ops: {self.channelObj.operators}, \
                has other bots: {self.channelObj.hasOtherBots}, \
                custom commands: {str( self.channelObj.customCommands.keys() ).replace("dict_keys", "")}'
            )
        else:
            self.chat.send('To perform this action mod permissions are required')
        

    async def evalPi(self, variable: str, sender: str):
        if self.channelObj.isop(sender):
            eval(variable)

    async def mod(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            self.channelObj.moderators.append(variable)
            self.channelObj.log(f'now {variable} is a moderator')
            self.chat.send(f'now {variable} is a moderator')
        else:
            self.chat.send('To perform this action mod permissions are required')

    async def demod(self, variable: str, sender: str):
        if self.channelObj.ismod(sender):
            self.channelObj.operators.remove(variable)
            self.channelObj.log(f'now {variable} is no longer a moderator')
            self.chat.send(f'now {variable} is no longer a moderator')
        else:
            self.chat.send('To perform this action mod permissions are required')
    
    async def op(self, variable: str, sender: str):
        if self.channelObj.isop(sender):
            self.channelObj.operators.append(variable)
            self.channelObj.log(f'now {variable} is an operator')
            self.chat.send(f'now {variable} is an operator')
        else:
            self.chat.send('To perform this action op permissions are required')

    async def deop(self, variable: str, sender: str):
        if self.channelObj.isop(sender): 
            self.channelObj.operators.remove(variable)
            self.channelObj.log(f'now {variable} is no longer an operator')
            self.chat.send(f'now {variable} is no longer an operator')
        else:
            self.chat.send('To perform this action op permissions are required')

    async def echo(self, variable: str,sender: str):
        if variable == '':
            self.chat.send('This command requires a variable')
            return
        elif ( variable.startswith('!') ) and ( not variable.startswith('!echo') ):
            return
        else:
            self.chat.send(variable)
            return
    