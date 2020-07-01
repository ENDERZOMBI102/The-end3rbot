import dotenv
import Channel

if __name__ == '__main__':
    dotenv.load_dotenv()
    
    cn = Channel.Channel('ENDERZOMBI102')

comBaseDocs: list = \
{
    'addCommand': 'add a custom command',
    'cmds': 'display this message',
    'help': 'display the help string of the specified command',
    'cs': 'change symbol for this channel, requires mod powers'
}

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
"""