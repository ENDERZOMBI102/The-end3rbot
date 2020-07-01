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
        

# TODO: implement old commands (those ones)
"""
def handler(message: twitch.chat.Message):
    elif command == 'addCommand':
        # check if sender is mod
        if not ( message.sender in operators or moderators ):
            chat.send("you're not a mod!")
            return  # its not, return
        # add a custom command
        customCommand.add(variable)
    elif command == 'cmds':
        chat.send('avaiable commands: help, ')
    elif command == 'cs':
        if not ( message.sender in operators or moderators ):
            return
        elif len(variable) > 1:
            chat.send('the symbol is max 1 character')
            return
        elif variable in ['', ' ']:
            chat.send('symbol not valid')
            return
        else:
            symbol = variable
            with open('channels.json', 'r') as file:
                channels = file.read()
            channels[channel]['symbol'] = symbol
            with open('channels.json', 'w') as file:
                json.dump(channels, file)
"""