def createChannelDict(channel: str) -> dict:
	channel = channel.lower()
	return {
		'channel': channel if '#' not in channel else channel.replace('#', '', 1),
		'hasOtherBots': False,
		'prefix': '!',
		'operators': [],
		'commands': {}
	}
