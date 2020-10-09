import json
import traceback
from typing import List

from twitchio import Message

import TwitchBotV2.Channel
from TwitchBotV2 import Channel


class stdCommandsHandler:
    
    commands: dict = \
    {
        'help': 'display the help string of the specified command',
        'addCommand': 'add a custom command, requires mod powers',
        'cmds': 'display this message',
        'cp': 'change prefix for this channel, requires mod powers',
        'saveChannelData': 'saves channel data to disk, requires op powers',
        'sendChannelData': 'send channel data to chat, requires mod powers',
        'evalPi': 'evaluate a py expression, requires op powers',
        'mod': 'makes the given user a mod, requires mod powers',
        'demod': 'makes the given user no longer an mod, requires mod powers',
        'op': 'makes the given user an op, requires op powers',
        'deop': 'makes the given user no longer an op, requires op powers',
        'echo': 'echo echo echo',
    }

    channel: Channel

    def __init__( self, channel: Channel ):
        self.channel = channel

    # commands declarations have this syntax:
    # async def COMMANDNAME (self, cmd: List[str], msg: Message )
    # where cmd are the parameters (if there's one) and is of type List[str]
    # where await msg.author.name is the username of the user that issued the command and is of type str

    async def help(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            await msg.channel.send("missing parameter <command>")
        elif cmd[0] in self.commands.keys():
            await msg.channel.send( self.commands[ cmd[0] ] )
        elif cmd[0] in self.channel.customCommandHandler.customCommands.keys():
            try:
                txt: str = self.channel.customCommandHandler.customCommands[ cmd[0] ]['help']
            except Exception as e:
                print(e.__class__)
                await msg.channel.send( "this command doesn't have a help string" )
            else:
                await msg.channel.send(txt)
        
    async def addCommand(self, cmd: List[str], msg: Message):
        # check if await msg.author.name is mod
        if self.channel.ismod(msg.author) is True:
            # add a custom command
            msg.content = msg.content.replace('!addCommand ', '', 1)
            if len( msg.content ) == 0:
                await msg.channel.send('missing parameter <commandjson>')
            else:
                await self.channel.customCommandHandler.add( msg )
                self.channel.save()
        else:
            await msg.channel.send('To perform this action mod permissions are required')

    async def cmds(self, cmd: List[str], msg: Message):
        await msg.channel.send(
            f'available commands: help, addCommand, cmds, cp, \
            saveChannelData, sendChannelData, evalPi, (de)mod, \
            (de)op'
        )
    
    async def cp(self, cmd: List[str], msg: Message):
        if self.channel.ismod(msg.author):
            if len(cmd) == 0:
                await msg.channel.send('missing parameter <prefix>')
            elif len(cmd[0]) > 1:
                await msg.channel.send('the prefix is max 1 character')
            elif cmd[0] in ['', ' ']:
                await msg.channel.send('prefix not valid')
            else:
                self.channel.prefix = cmd[0]
                await msg.channel.send(f'prefix has been changed to {cmd[0]}')
                self.channel.save()
        else:
            await msg.channel.send('To perform this action mod permissions are required')

    async def saveChannelData(self, cmd: List[str], msg: Message):
        if self.channel.isop(msg.author.name):
            self.channel.save()
        else:
            await msg.channel.send('To perform this action op permissions are required')

    async def evalPi(self, cmd: List[str], msg: Message):
        if self.channel.isop(msg.author.name):
            if len(cmd) == 0:
                await msg.channel.send('missing parameter <code>')
            else:
                try:
                    eval( ' '.join(cmd) )
                except Exception as e:
                    await msg.channel.send( traceback.format_exception( type(e), e, e.__traceback__ ) )

    async def mod(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            await msg.channel.send('missing parameter <user>')
        elif self.channel.ismod(msg.author):
            await msg.channel.send(fr'\mod {cmd[0]}')
            self.channel.log(f'now {cmd[0]} is a moderator')
            await msg.channel.send(f'now {cmd[0]} is a moderator')
        else:
            await msg.channel.send('To perform this action mod permissions are required')

    async def demod(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            await msg.channel.send('missing parameter <user>')
        elif self.channel.ismod(msg.author):
            self.channel.operators.remove(cmd[0])
            self.channel.log(f'now {cmd[0]} is no longer a moderator')
            await msg.channel.send(f'now {cmd[0]} is no longer a moderator')
        else:
            await msg.channel.send('To perform this action mod permissions are required')
    
    async def op(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            await msg.channel.send('missing parameter <user>')
        elif self.channel.isop(msg.author.name):
            self.channel.operators.append(cmd[0])
            self.channel.log(f'now {cmd[0]} is an operator')
            await msg.channel.send(f'now {cmd[0]} is an operator')
        else:
            await msg.channel.send('To perform this action op permissions are required')

    async def deop(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            await msg.channel.send('missing parameter <user>')
        elif self.channel.isop(msg.author.name):
            self.channel.operators.remove(cmd[0])
            self.channel.log(f'now {cmd[0]} is no longer an operator')
            await msg.channel.send(f'now {cmd[0]} is no longer an operator')
        else:
            await msg.channel.send('To perform this action op permissions are required')

    async def echo(self, cmd: List[str], msg: Message):
        if len( cmd ) == 0:
            if self.channel.poetMode:
                await msg.channel.send(
                    'Be or not be, this is the problem, in the emptiness of this earth i live... \
                    idk what am i saying, you forgot the parameter you dumb'
                )
            else:
                await msg.channel.send('This command requires a variable')
        elif cmd[0].startswith('!'):
            if not cmd[0].startswith('!echo'):
                return
        await msg.channel.send(' '.join(cmd))

    async def poetMode(self, cmd: List[str], msg: Message):
        self.channel.poetMode = not self.channel.poetMode
