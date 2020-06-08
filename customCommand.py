import json
import twitch
import keyboard
import requests as req

chat: twitch.Chat


customCommandsData = {}
commandList = {
    'exampleCommand' : {
        'text' : 'this is an example {url}',
        'data' : {
            'url' : 'https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/.gitignore'
        }
    },
    'exampleCommand2' : {
        'text' : 'this is another example {}',
        'data' : {
            'urljson' : '',
            'sections': ['first', 'second']
        }
    }
}


def init(c: twitch.Chat):
    chat = c
    with open('./commands.json', 'r') as file:
        commandList = json.load(file)


def add( strdata: str ) -> None:
    try:
        data: dict = json.loads(strdata)
    except:
        chat.send(
            'to add a command, write a json with those values: name (command name),' +
            ' send (send a message, {ext rersource}), get (gets a resource)' +
            ''
        )
        return
    del strdata
    chat.send('checking syntax..')
    # check if it is already defined before checking the command
    if data['name'] in commandList.keys():
        chat.send('you can\'t overwrite a command!')
        return
    # this section check the command syntax
    #  send check
    if 'send' in data.keys():
        if len(data['send']) < 1:
            chat.send('send value must be at least 1 character')
            return
    #  press check
    if 'press' in data.keys():
        if len(data['press']) > 3:
            chat.send(f'{data["press"]} is not a valid key')
            return
    #  paramReplace check
    if 'paramReplace' in data.keys():
        if 'send' not in data.keys():
            chat.send('no "send" key provided, "paramReplace" is dependant on "send".')
            return
        if data['paramReplace'] not in data['send']:
            chat.send(f'paramReplace value {data["paramReplace"]} not in send value')
            return
    #  canBeUsedBy check
    if 'canBeUsedBy' in data.keys():
        if data['canBeUsedBy'] not in ['everyone', 'mod', 'op', 'streamer']:
            chat.send(f'{data["canBeUsedBy"]} is not a valid value, the value can be: everyone, mod, op, streamer ')
            return
    #  data components
    if 'data' in data.keys():
        #  url check
        if 'url' in data['data'].keys():
            if not data['data']['url'].startswith('https'):
                chat.send('the bot only supports the HTTPS protocol')
                return
        #  urljson check
        if 'urljson' in data['data'].keys():
            if 'sections' not in data['data']:
                chat.send('no "sections" key in data')
                return
            if not data['data']['urljson'].startswith('https'):
                chat.send('the bot only supports the HTTPS protocol')
                return
        #  sections check
        if 'sections' in data['data']:
            if len(data['data']['sections']) is 0:
                chat.send('no sections specified')
                return
            elif len(data['data']['sections']) > 2:
                chat.send('too many sections in "sections"')
                return
        #  load check
        if 'load' in data['data']:
            if '{var}' in data['send']:
                chat.send('no "{var}" in "send" value ('+data['send']+')')
                return
    name = data['name']  # save the command name
    del data['name']  # delete the name key
    commandList[name] = data  # create the command under the command name
    with open('./commands.json', 'w') as file:  # save all in the config file
        json.dump(commandList, file, indent=4)
    chat.send(f'command "{name}" successfully added')  # send success notice


# this is the function that take care of command execution
# TODO: order please!
# TODO: add key pressing as action
def execute( command: str, variable: str = None ):
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
    comDict: dict = commandList[command]
    del command
    # if the command should have a parameter and it doesn't, send an error
    # variable checks
    if 'needVar' in comDict.keys():  # check if the command needs a variable
        if comDict['needVar'] is True:
            if variable is not None:  # variable?
                pass  # yes
            else:
                chat.send('this command needs a parameter.')  # no
                return
    if 'varIsPing' in comDict.keys():  # check if the variable needs to be a ping
        if comDict['varIsPing'] is True:
            if variable.startswith('@'):  # is mention?
                pass  # yes
            else:
                chat.send('this command needs a mention as parameter.')
                return  # no
    # data operations
    #  url action
    if 'data' in comDict.keys():
        if 'url' in comDict['data'].keys():
            try:
                comDict['send'] = comDict['send'].replace('{url}', req.get(comDict['data']['url']).text)
            except Exception as e:
                chat.send(f'An error occurred while processing "url": {e}')
                print(comDict)
                return  # error!
        #  urljson action
        if 'urljson' in comDict['data'].keys():
            try:
                data = req.get(comDict['data']['url']).json()
            except Exception as e:
                chat.send(f'An error occurred while processing "urljson": {e}')
                return  # error!
            if len(comDict['data']['sections']) == 1:  # 1 section
                comDict['send'] = comDict['send'].replace(  # replace
                    '{urljson}',  # what to replace
                    data[comDict['data']['sections'][0]]  # replace with
                )
            else:  # two sections
                comDict['send'] = comDict['send'].replace(  # replace
                    '{urljson}',  # what to replace
                    data[comDict['data']['sections'][0]][comDict['data']['sections'][1]]  # replace with
                )
        # load action
        if 'load' in comDict['data'].keys():
            try:
                comDict['send'] = comDict['send'].replace(
                    '{var}',
                    customCommandsData[comDict['data']['load']]
                )
            except:
                chat.send(f'An error occurred while processing "load": no variable named {comDict["data"]["load"]}')
                return  # error!
        # saveAs action
        if 'saveAs' in comDict['data'].keys():
            saveData: list = comDict['data']['saveAs']  # for semplicity
            if len(saveData) == 1:
                customCommandsData[saveData[0]] = variable
            elif len(saveData) == 2:
                customCommandsData[saveData[0]] = req.get(saveData[1]).text
            else:
                chat.send('too many values for "saveAs"! no variable has been saved!')
                return
            del saveData  # no survivors :)
    # paramReplace action
    if 'paramReplace' in comDict.keys():
        comDict['send'] = comDict['send'].replace(comDict['paramReplace'], variable)
    # press action
    if 'press' in comDict.keys():
        keyboard.press_and_release(comDict['press'])
    # send action
    if 'send' in comDict.keys():
        chat.send(comDict['send'])