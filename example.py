"""
a command object that contains all the possible options
    {
        "send": "",
        "press": "",
        "varIsPing": true,
        "needVar": true,
        "paramReplace": "",
        "canBeUsedBy": "", # everyone, op, mod, streamer
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
    "varIsPing": true, // this can be omitted, this makes the command strip the @
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