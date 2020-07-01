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
        if not ( sender in self.channelObj.operators or self.channelObj.moderators ):
            self.chat.send("you're not a mod!")
            return  # its not, return
        # add a custom command
        customCommand.add(variable)

    async def cmds(self, variable: str, sender: str):
        self.chat.send(f'avaiable commands: addCommand, cmds, help, cs')
    
    async def cs(self, variable: str, sender: str):
        if not ( sender in self.channelObj.operators or self.channelObj.moderators ):
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