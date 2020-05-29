from bot import customCommands, chat, customCommandsData
import json
import requests as req


def addCustomCommand( data: str = None ):
    try:
        data = json.loads(data)
    except:
        chat.send(
            'to add a command, write a json with those values: name (command name),' +
            ' send (send a message, {ext rersource}), get (gets a resource)' +
            ''
        )
    if data['name'] in customCommands:
        chat.send('you can\'t overwrite a command!')
        return
    name = data['name']
    del data['name']
    customCommands[name] = data
    with open('./commands.json', 'w') as file:
        json.dump(customCommands, file, indent=4)


# TODO: order please!
# TODO: add key pressing as action
def customCommand( command: str = None ):
    comDict = customCommands[command]
    if 'get' in comDict.keys():
        if 'url' in comDict['get'].keys():
            data = req.get(comDict['get']['url']).text
        elif 'urljson' in comDict['get'].keys():
            if not 'sections' in comDict['get'].keys():
                chat.send('you didn\'t put a "sections" section in the "get" action!')
                return
            if len(comDict['get']['sections']) == 2:
                data = req.get(comDict['get']['url']).json()[comDict['get']['sections'][0]][comDict['get']['sections'][1]]
            elif len(comDict['get']['sections']) == 1:
                data = req.get(comDict['get']['url']).json()[comDict['get']['sections'][0]]
        elif 'load' in comDict['get'].keys():
            if not customCommandsData[comDict['get']['load']]:
                chat.send(f'data {comDict["get"]["load"]} doens\'t exist!')
                return
            data = customCommandsData[comDict['get']['load']]
    if 'send' in comDict.keys():
        try:
            print(data)
            chat.send( comDict['send'].replace( '{}', data ) )
            print('sended')
        except Exception as e:
            print(f'ERROR: {e}')
            chat.send( comDict['send'] )


class CustomCommand:
    def __init__(self, commandData: dict = None, param = None):
        # the text
        try: self.text = commandData['send']
        except: self.text = None
        # replace the text with parameter
        try: self.text = self.text.replace('{}', param)
        except: self.text = None


    def send(self):
        chat.send(self.text)

    def get(self):


"""
a command dict that contains all the possible options
    {
        "send": "",
        "press": "",
        "paramReplace": "",
        "get": {
            "url": "",
            "urljson": "",
            "sections": []
        }
    }

"""

