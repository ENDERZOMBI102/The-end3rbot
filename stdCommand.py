import twitch
import keyboard
import asyncio
import json
import os
import customCommand
import typing

class stdCommandsHandler:
    
    commands: list = \
    {
        'addCommand': 'add a custom command',
        'cmds': 'display this message',
        'help': 'display the help string of the specified command',
        'cs': 'change symbol for this channel, requires mod powers'
    }


    def __init__(self):
        pass