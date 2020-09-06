import twitchio.dataclasses
from os import getenv
from typing import List
import TwitchBotV2.customCommand as customCommand


class Channel:

    # data
    channel: str
    hasOtherBots: bool
    prefix: str
    moderators: List[str]
    operators: List[str]
    client: twitchio.Client
    chat: twitchio.dataclasses.Channel

    def __init__(self, channelData: dict):
        self.channel = channelData['channel']
        self.hasOtherBots = channelData['hasOtherBots']
        self.prefix = channelData['prefix']
        self.moderators = channelData['moderagors']
        self.operators = channelData['operators']
        self.client = twitchio.Client( client_id=getenv('TWITCH_CLIENT_ID') )
        self.chat = twitchio.dataclasses.Channel(channel)
        self.customCommandHandler = customCommand.customCommandsHandler(self.chat, channelData['commands'])
        
        



    def __str__(self):
        return {
            'channel': self.channel,
            'hasOtherBots': self.hasOtherBots,
            'prefix': self.prefix,
            'moderators': self.moderators,
            'operators': self.operators,
            'commands': self.customCommandHandler.commands
        }
        