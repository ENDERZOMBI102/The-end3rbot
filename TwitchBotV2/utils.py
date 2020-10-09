

def createChannelDict(channel: str) -> dict:
        channel = channel.lower()
        return {
            {
                'channel' : f'#{channel}' if '#' not in channel else channel,
                'hasOtherBots' : False,
                'prefix' : '!',
                'moderators' : [],
                'operators'  : [
                    channel
                ],
                'customCommands' : {}
            }
        }
