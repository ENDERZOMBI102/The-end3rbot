import twitch
import keyboard
import asyncio
import json
import os
import requests as req
from typing import Union, Any
import typing


symbol = '!'
timeout = False
counter: int = 0

customCommands = \
{
    'exampleCommand' : {
        'text' : 'this is an example {url}',
        'get' : {
            'url' : 'https'
        }
    },
    'exampleCommand2' : {
        'text' : 'this is another example {json url}',
        'get' : {
            'urljson' : '',
            'sections': ['first', 'second']
        }
    }
}


customCommandsData = {}




def handler(message: twitch.chat.Message):
    if not message.text.startswith(symbol): return
    text = message.text.replace(symbol, '', 1)
    command, variable = text.split(' ', 1)
    hasPing = '@' in text
    print(f' command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {command in customCommands}')
    if command in customCommands:
        customCommand(command)
        return
    if command == 'pause':
        if not timeout:
            asyncio.run(waitForTimeout())
            keyboard.press_and_release('esc')
        else:
            chat.send(f'can\' run that! wait {counter} seconds more!')
    if command == 'addCommand':
        addCustomCommand(variable)

def addCustomCommand( data: str = None ):
    try:
        data = json.loads(data)
    except:
        chat.send(
            'to add a command, write a json with those values: name (command name),' +
            ' send (send a message, {ext rersource}), get (gets a resource)' +
            ''
        )
    if data['name'] in customCommands:
        chat.send('you can\'t overwrite a command!')
        return
    name = data['name']
    del data['name']
    customCommands[name] = data


def customCommand( command: str = None ):
    comDict = customCommands[command]
    if 'get' in comDict.keys():
        if 'url' in comDict['get'].keys():
            data = req.get(comDict['get']['url'])
        elif 'urljson' in comDict['get'].keys():
            if not 'sections' in comDict['get'].keys():
                chat.send('you didn\'t put a "sections" section in the "get" action!')
                return
            if len(comDict['get']['sections']) == 2:
                data = req.get(comDict['get']['url']).json()[comDict['get']['sections'][0]][comDict['get']['sections'][1]]
            elif len(comDict['get']['sections']) == 1:
                data = req.get(comDict['get']['url']).json()[comDict['get']['sections'][0]]
        elif 'load' in comDict['get'].keys():
            if not customCommandsData[comDict['get']['load']]:
                chat.send(f'data {comDict["get"]["load"]} doens\'t exist!')
                return
            data = customCommandsData[comDict['get']['load']]
    if 'send' in comDict.keys():
        chat.send(comDict['send'].replace(r'{}'))
    #if


async def waitForTimeout():
    global timeout
    timeout = True
    await counter()
    timeout = False


async def count(seconds: int = 10):
    global counter
    while counter != seconds:
        await asyncio.sleep(1)
        counter += 1
    counter = 0


if __name__ == '__main__':
    print('Welcome to ENDERZOMBI102\'s bot, The end3rbot!')
    channel = '#' + input('To start the bot, insert your channel name: ').lower()
    if channel == '': channel = '#enderzombi102'
    chat = twitch.Chat(channel=channel,
                       nickname=os.getenv('USERNAME'),
                       oauth=os.getenv('OAUTH_TOKEN')
                       )
    chat.subscribe(handler)
    chat.send('The end3rbot successfully connected')