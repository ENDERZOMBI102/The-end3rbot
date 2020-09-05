import sys
if '--twitchv2' in sys.argv:
    import TwitchBotV2 as TwitchBot
else:
    import TwitchBot
import DiscordBot
import dotenv
from typing import List

dotenv.load_dotenv()

if __name__ == '__main__':
    # discordClient = DiscordBot.Client()
    # discordClient.run()
    botInstances: List[TwitchBot.Channel] = [
        TwitchBot.Channel('ENDERZOMBI102'),
        TwitchBot.Channel('AllSoTuff'),
    ]
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
        elif com == 'help':
            print('avaiable commands:')
            print('q            turn off all instances and quits the bot')
            print('add PARA     create an instance for channel PARA')
            print('off PARA     turns off PARA\'s channel instance')
            print('help         display this screen')
        else:
            print(f'unknown CLI command: {com}')