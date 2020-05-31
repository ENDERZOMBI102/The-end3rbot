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
def customCommand( comDict: dict = None, variable: str = None ):
    # if the command should forcily have a parameter and it doesn't, send an error
    try:
        if ( comDict['needVar'] is True ) and ( variable is None ):
            chat.send('ERROR, expected parameter')


"""
a command object that contains all the possible options
    {
        "send": "",
        "press": "",
        "varIsPing": true,
        "needVar": true,
        "paramReplace": "",
        "canBeUsedBy": "", # everyone, mod, streamer
        "data": {
            "url": "",
            "urljson": "",
            "sections": [],
            "load" : "varname",
            "saveAs" : ["varName", "url"]
        }
    }

this is an example implementing a ban command
{
    "send": "/ban {}",
    "varIsMention": true, // this can be omitted, this makes the command strip the @
    "needVar": true,
    "paramReplace" : "{}"
}
this is an example implementing a "whats the latest version of" command
{
    "send": "latest version of {0} is: {}",
    "paramReplace" : "{0}",
    "needVar" : true,
    "data": {
        "urljson": "paramVar",
        "sections": ["tag_name"]
    }
}
"""

