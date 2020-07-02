import json
import twitch
import keyboard
import requests as req


class customCommandsHandler:

    # twitch chat
    chat: twitch.Chat
    # current channel name
    channel: str
    # custom commands data
    customCommandsData: dict

    def __init__( self ):
        pass

    def addChannelObj( self, channelObj ) -> None:
        import Channel
        # channel object
        self.channelObj: Channel.Channel = channelObj

    async def add( self, strdata: str ) -> None:
        try:
            data: dict = json.loads(strdata)
        except:
            self.chat.send(
                'to add a command, write a json with those values: name (command name),' +
                ' send (send a message, {ext rersource}), get (gets a resource)' +
                ''
            )
            return
        del strdata
        self.chat.send('checking syntax..')
        # check if it is already defined before checking the command
        if data['name'] in self.channelObj.customCommands.keys():
            self.chat.send('you can\'t overwrite a command!')
            return
        # this section check the command syntax
        #  send check
        if 'send' in data.keys():
            if len(data['send']) < 1:
                self.chat.send('send value must be at least 1 character')
                return
        #  press check
        if 'press' in data.keys():
            if len(data['press']) > 3:
                self.chat.send(f'{data["press"]} is not a valid key')
                return
        #  paramReplace check
        if 'paramReplace' in data.keys():
            if 'send' not in data.keys():
                self.chat.send('no "send" key provided, "paramReplace" is dependant on "send".')
                return
            if data['paramReplace'] not in data['send']:
                self.chat.send(f'paramReplace value {data["paramReplace"]} not in send value')
                return
        #  canBeUsedBy check
        if 'canBeUsedBy' in data.keys():
            if data['canBeUsedBy'] not in ['everyone', 'mod', 'op', 'streamer']:
                self.chat.send(f'{data["canBeUsedBy"]} is not a valid value, the value can be: everyone, mod, op, streamer ')
                return
        #  data components
        if 'data' in data.keys():
            #  url check
            if 'url' in data['data'].keys():
                if not data['data']['url'].startswith('https'):
                    self.chat.send('the bot only supports the HTTPS protocol')
                    return
            #  urljson check
            if 'urljson' in data['data'].keys():
                if 'sections' not in data['data']:
                    self.chat.send('no "sections" key in data')
                    return
                if not data['data']['urljson'].startswith('https'):
                    self.chat.send('the bot only supports the HTTPS protocol')
                    return
            #  sections check
            if 'sections' in data['data']:
                if len(data['data']['sections']) == 0:
                    self.chat.send('no sections specified')
                    return
                elif len(data['data']['sections']) > 2:
                    self.chat.send('too many sections in "sections"')
                    return
            #  load check
            if 'load' in data['data']:
                if '{var}' in data['send']:
                    self.chat.send('no "{var}" in "send" value ('+data['send']+')')
                    return
        if 'evalPi' in data.keys():
            self.chat.send('WARNING: evalPi action is present! that requires op powers!')
        if 'name' not in data.keys():
            self.chat.send('you forgot the command name..')
            return
        name = data['name']  # save the command name
        del data['name']  # delete the name key
        self.chat.send(f'syntax validated! added command {name}')
        self.channelObj.customCommands[name] = data  # create the command under the command name
        self.chat.send(f'command "{name}" successfully added')  # send success notice

    # this is the function that take care of command execution
    async def execute( self, command: str, variable: str, sender: str):
        """
        :param command: command name to execute
        :param variable: command variable
        """
        """
        an action is usually build like this:
        if 'actionkey' in comDict.keys() # to check if its in the command
            -action operations-
            if error: # metaphor for error catching
                chat.send('error message') # send error info, example: 'you forgot a parameter'
                return # 'return because its an error, cannot continue
        
        """
        comDict: dict = self.channelObj.customCommands[command]
        del command
        # to be sure that a new string is created and that we don't use the one in the dict
        text = str(comDict['send']) or ''
        # first check of all: canBeUsedBy, cuz if the user can't execute it, why bother?
        if 'canBeUsedBy' in comDict.keys():
            validUser = comDict['canBeUsedBy']
            if validUser == 'everyone':  # can be used by everyone
                pass
            elif validUser == 'op':  # can be used by channel operators
                if sender not in self.channelObj.operators:
                    return
            elif validUser == 'mod':  # can be used by channel moderators
                if sender not in self.channelObj.moderators:
                    return
            elif validUser == 'streamer':   # can be used by streamer
                if not sender.lower() == channel.lower().replace('#', ''):
                    return
            else:
                self.chat.send(f'ERROR: unknown "canBeUsedBy" value {validUser}')
            del validUser
        # if the command should have a parameter and it doesn't, send an error
        # variable checks
        if 'needVar' in comDict.keys():  # check if the command needs a variable
            if comDict['needVar'] is True:
                if variable is not None:  # variable?
                    pass  # yes
                else:
                    self.chat.send('this command needs a parameter.')  # no
                    return
        if 'varIsPing' in comDict.keys():  # check if the variable needs to be a ping
            if comDict['varIsPing'] is True:
                if variable.startswith('@'):  # is mention?
                    pass  # yes
                else:
                    self.chat.send('this command needs a mention as parameter.')
                    return  # no
        if 'send' in comDict.keys():
            if r'{para}' in comDict['send']:
                text = text.replace(r'{para}', variable)
            if r'{sender}' in comDict['send']:
                text = text.replace(r'{sender}', sender)
        # data operations
        #  url action
        if 'data' in comDict.keys():
            if 'url' in comDict['data'].keys():
                try:
                    text = text.replace('{url}', req.get(comDict['data']['url']).text)
                except Exception as e:
                    self.chat.send(f'An error occurred while processing "url": {e}')
                    return  # error!
            #  urljson action
            if 'urljson' in comDict['data'].keys():
                try:
                    data = req.get(comDict['data']['url']).json()
                except Exception as e:
                    self.chat.send(f'An error occurred while processing "urljson": {e}')
                    return  # error!
                if len(comDict['data']['sections']) == 1:  # 1 section
                    text = text.replace(  # replace
                        '{urljson}',  # what to replace
                        data[comDict['data']['sections'][0]]  # replace with
                    )
                else:  # two sections
                    text = text.replace(  # replace
                        '{urljson}',  # what to replace
                        data[comDict['data']['sections'][0]][comDict['data']['sections'][1]]  # replace with
                    )
            # load action
            if 'load' in comDict['data'].keys():
                try:
                    text = text.replace(
                        '{var}',
                        customCommandsData[comDict['data']['load']]
                    )
                except:
                    self.chat.send(f'An error occurred while processing "load": no variable named {comDict["data"]["load"]}')
                    return  # error!
            # saveAs action
            if 'saveAs' in comDict['data'].keys():
                saveData: list = comDict['data']['saveAs']  # for semplicity
                if len(saveData) == 1:
                    customCommandsData[saveData[0]] = variable
                elif len(saveData) == 2:
                    customCommandsData[saveData[0]] = req.get(saveData[1]).text
                else:
                    self.chat.send('too many values for "saveAs"! no variable has been saved!')
                    return
                del saveData  # no survivors :)
        # press action
        if 'press' in comDict.keys():
            keyboard.press_and_release(comDict['press'])
        # send action
        if 'send' in comDict.keys():
            self.chat.send(text)
        if ( 'evalPi' in comDict.keys() ) and ( self.channelObj.isop(sender) ):
            eval(comDict['evalPi'])