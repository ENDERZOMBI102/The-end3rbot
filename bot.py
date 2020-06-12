import twitch
import keyboard
import asyncio
import json
import os
import customCommand
import dotenv

# TODO: use classes!

symbol = '!'
timeout = False
counter: int = 0
channel: str = 'CHANNEL_1'
operators: list
moderators: list
chat: twitch.Chat = None
comBaseDocs: list = \
{
    'addCommand': 'add a custom command',
    'cmds': 'display this message',
    'help': 'display the help string of the specified command',
    'cs': 'change symbol for this channel, requires mod powers'
}
comDocs: list


def handler(message: twitch.chat.Message):
    global symbol
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
        customCommand.execute(command, variable, message.sender)
        return
    # not a custom command, use normal handler
    elif command == 'addCommand':
        # add a custom command
        customCommand.add(variable)
    elif command == 'cmds':
        chat.send('avaiable commands: help, ')
    elif command == 'help':
        if variable in ['', ' ']:
            return
        if variable in comBaseDocs.keys():
            chat.send(comBaseDocs[variable])
        elif variable in customCommand.commandList.keys():
            chat.send(customCommand.commandList[variable])
        else:
            chat.send(f'command {command} not found')
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
    with open('channels.json', 'r') as file:
        channels = json.load(file)
    if channel not in channels:
        channels[channel] = \
            {
                'operators' : [channel.replace('#', '')],
                'moderators' : [channel.replace('#', '')],
                'symbol' : '!'
            }
        with open('channels.json', 'w') as file:
            json.dump(channels, file, indent=4)
    operators = channels[channel]['operators']
    moderators = channels[channel]['moderators']
    symbol = channels[channel]['symbol']
    del channels  # no useless data
    customCommand.init(chat, operators, moderators, channel)  # init custom commands module
    print('ready!')
    chat.send('The end3rbot successfully connected')