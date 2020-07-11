import TwitchBot
import DiscordBot
import dotenv

dotenv.load_dotenv()

if __name__ == '__main__':
    #discordClient = DiscordBot.Client()
    #discordClient.run()
    cn0 = TwitchBot.Channel('ENDERZOMBI102')
    cn1 = TwitchBot.Channel('AllSoTuff')
    cn2 = TwitchBot.Channel('baguettery')
    """while True:
        try:
            print( eval( input('The_end3rbot>') ) )
        except Exception as e:
            if e is not None:
                print(e)"""