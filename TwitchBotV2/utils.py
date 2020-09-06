

def createChannelDict(channel: str) -> dict:
        channel = channel.lower()
        if '#' in channel:
            channel = channel.replace('#','')
        return {
            f'#{channel}' : {
                'symbol' : '!',
                'hasOtherBots' : False,
                'moderators' : [
                    
                ],
                'operators'  : [
                    channel
                ],
                'customCommands' : {

                }
            }
        }
