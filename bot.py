import twitch
import keyboard
import asyncio
import json
import os
import customCommand
import dotenv


symbol = '!'
timeout = False
counter: int = 0
channel: str = 'CHANNEL_1'
operators: list
moderators: list
chat: twitch.Chat = None


def handler(message: twitch.chat.Message):
    # if the message doesn't start with SYMBOL is not a command
    if not message.text.startswith(symbol): return
    # remove the SYMBOL
    text = message.text.replace(symbol, '', 1)
    # if there's a variable, take it
    try:
        command, variable = text.split(' ', 1)
    except:
        command, variable = text, None
    # if there's a @ has a mentions
    hasPing = '@' in text
    # is a custom command?
    isCustom = command in customCommand.commandList
    # print command infos
    print(f' command: {command}, variable: {variable}, has ping: {hasPing}, is custom: {isCustom}')
    if isCustom:
        # is a custom command, execute it with the cc handler
        customCommand.execute(command, variable, message)
        return
    # not a custom command, use normal handler
    elif command == 'pause' and os.getenv('CHANNEL') is '#enderzombi102':
        if not timeout: # press esc!
            asyncio.run( waitForTimeout() )
            keyboard.press_and_release('esc')
        else:
            # timer is still running!
            chat.send(f'can\' run that! wait {counter} seconds more!')
    elif command == 'addCommand':
        # add a custom command
        customCommand.add(variable)

    elif command == 'minecraft':
        chat.send('ikr, tuff should play minecraft!')


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
    channel = os.getenv(channel).lower()
    chat = twitch.Chat(
        channel=channel,
        nickname=os.getenv('USERNAME'),
        oauth=os.getenv('OAUTH_TOKEN')
    )
    chat.subscribe(handler)
    with open('./channels.json', 'r') as file:
        channels = json.load(file)
    if channel not in channels:
        channels[channel] = \
            {
                'operators' : [channel.replace('#', '')],
                'mods' : [channel.replace('#', '')],
                'symbol' : '!'
            }
        with open('./channels.json', 'w') as file:
            json.dump(channels, file)
    operators = channels[channel]['operators']
    moderators = channels[channel]['moderators']
    del channels  # no useless data
    customCommand.init(chat, operators, moderators)  # init custom commands module
    print('ready!')
    chat.send('The end3rbot successfully connected')