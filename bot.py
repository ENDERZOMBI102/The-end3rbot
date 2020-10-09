import dotenv

import TwitchBotV2 as TwitchBot


dotenv.load_dotenv()


twitchBot = TwitchBot.Client()
twitchBot.run()

exit()
# the cli doesn't work :'(
print('you can now use the CLI')
while True:
	inp = input('').split(' ', 1)
	try:
		com, var = inp
	except Exception as e:
		com, var = inp[0], ''
		print(e.__class__)
	if com == 'q':
		print('bye!')
		exit()
	elif com == 'add':
		twitchBot.channels.append( TwitchBot.Channel.create(var) )
		print(f'turned on instance {var}')
	elif com == 'tgl':
		for channel in twitchBot.channels:
			if channel.name == var.lower():
				channel.disabled = not channel.disabled
				print(f'turned off instance {var}')
				break
	elif com == 'help':
		print('avaiable commands:')
		print('q            turn off all instances and quits the bot')
		print('add PARA     create an instance for channel PARA')
		print('tgl PARA     toggles PARA\'s channel instance')
		print('help         display this screen')
	else:
		print(f'unknown CLI command: {com}')
