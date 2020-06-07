import twitch
import keyboard
import asyncio
import json
import os
from customCommand import *
import dotenv


symbol = '!'
timeout = False
counter: int = 0
chat: twitch.Chat
user: str = '#enderzombi102'


def handler(message: twitch.chat.Message):
    # if the message doesn't start with SYMBOL is not a command
    if not message.text.startswith(symbol): return
    # remove the SYMBOL
    text = message.text.replace(symbol, '', 1)
    # if there's a variable, take it
    try:
        command, variable = text.split(' ', 1)
    except:
        command, variable = text, ''
    # if there's a @ has a mentions
    hasPing = '@' in text
    # is a custom command?
    isCustom = command in customCommands
    # print command infos
    print(f' command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {isCustom}')
    if isCustom:
        # is a custom command, execute it with the cc handler
        customCommand(customCommands[command], variable)
        return
    # not a custom command, use normal handler
    if command == 'pause' and os.getenv('CHANNEL') is '#enderzombi102':
        if not timeout: # press esc!
            asyncio.run( waitForTimeout() )
            keyboard.press_and_release('esc')
        else:
            # timer is still running!
            chat.send(f'can\' run that! wait {counter} seconds more!')
    if command == 'addCommand':
        # add a custom command
        addCustomCommand(variable)

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
    dotenv.load_dotenv()
    chat = twitch.Chat(channel=os.getenv('CHANNEL').lower(),
                       nickname=os.getenv('USERNAME'),
                       oauth=os.getenv('OAUTH_TOKEN')
                       )
    chat.subscribe(handler)
    with open('./commands.json', 'r') as file:
        customCommands = json.load(file)
    print('ready!')
    chat.send('The end3rbot successfully connected')