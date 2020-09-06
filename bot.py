import TwitchBotV2 as TwitchBot
import DiscordBot
import twitch.chat.message
import dotenv
import json
from pathlib import Path
from typing import List

dotenv.load_dotenv()


path = Path('./channels.json')
if not path.exist():
    



while True:
    inp = tuple( input('The_end3rbot> ').split(' ', 1) )
    try:
        com, var = inp
    except:
        com, var = inp[0], ''
    if com == 'q':
        print(f'turning off {len(botInstances)} instances...')
        botInstances.clear()
        print('bye!')
        exit()
    elif com == 'add':
        botInstances.append( TwitchBot.Channel(var) )
        print(f'turned on instance {var}')
    elif com == 'off':
        for i in range( len( botInstances ) ):
            if botInstances[i].channel == var.lower():
                del botInstances[i]
                print(f'turned off instance {var}')
                break
    elif com == 'help':
        print('avaiable commands:')
        print('q            turn off all instances and quits the bot')
        print('add PARA     create an instance for channel PARA')
        print('off PARA     turns off PARA\'s channel instance')
        print('help         display this screen')
        print('exec CNL PAR executes PAR on channel CNL')
    elif com == 'exec':
        CNL, PAR = var.split(' ', 1)
        for instance in botInstances:
            if instance.channel == CNL:
                msg = twitch.chat.message.Message(CNL, 'SYSTEM', PAR)
                instance.preCommandHandler(msg)
                break
        else:
            print(f'channel {CNL} is not a valid channel')
    else:
        print(f'unknown CLI command: {com}')