import json
import keyboard
import requests as req
from bot import chat


customCommandsData = {}
customCommands = {
    'exampleCommand' : {
        'text' : 'this is an example {url}',
        'get' : {
            'url' : 'https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/.gitignore'
        }
    },
    'exampleCommand2' : {
        'text' : 'this is another example {}',
        'get' : {
            'urljson' : '',
            'sections': ['first', 'second']
        }
    }
}


def addCustomCommand( strdata: str ) -> None:
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
    if data['name'] in customCommands:
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
    customCommands[name] = data  # create the command under the command name
    with open('./commands.json', 'w') as file:  # save all in the config file
        json.dump(customCommands, file, indent=4)
    chat.send(f'command "{name}" successfully added')  # send success notice


# this is the function that take care of command execution
# TODO: order please!
# TODO: add key pressing as action
def customCommand( comDict: dict = None, variable: str = None ):
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
                chat.send('this command needs a parameter.')
                return  # no
    if

