import discord
import DiscordBot.customCommand
import DiscordBot.stdCommand
import json


class Client(discord.Client):

    guilds: dict = {}

    async def on_ready(self):
        print('Logged on as', self.user)
        print('loading guils..')
        await self.loadGuilds()
        

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if not message.guild:
            return

    def loadGuilds( self ):
        with open('./guilds.json', 'r') as file:
            guildData = json.load(file)
        for guild in guildData:
            identifier: str = guild['id']
            self.guilds[identifier][name] = guild['name']
            self.guilds[identifier]['moderators'] = guild['moderators']
            self.guilds[identifier]['operators'] = guild['operators']
            