Custom Commands Docs
-
Custom Commands are a powerful feature of this bot, they can do almost anything, from
sending a command to press a key on your keyboard.<br>
and they're simple as json! (hjson support coming soon)

for a description of the terms used in this document see [dictionary]()

|section|value|parent|depends on|
|-------|-----|------|----------|
|[send]()|string|none|none|
|[press]()|string/char|none|none|
|[varIsPing]()|boolean|none|parameter|
|[needVar]()|boolean|none|parameter|
|[paramReplace]()|string|none|send, parameter|
|[canBeUsedBy]()|string|none|none|
|[data]()|object|none|- - - - - - -|
|[url]()|string|data|send|
|[urljson]()|string|data|send, sections|
|[sections]()|array(string)|data|urljson|
|[load]()|string|data|send|
|[saveAs]()|array(string)|data|parameter|

send
-
example:
```json
{
  "send": "this is text"
}
```
this section holds the text that the command will send,
it can have text substitution with {} and data actions

press
-
example:
```json
{
  "press": "esc"
}
```
this section makes the command press the key that is passed on the keyboard

varIsPing
-
example:
```json
{
  "varIsPing" : true
}
```
this makes the command remove the @ in the parameter's mention/ping so it can be used in twitch commands
like /ban or /mod

needVar
-
example:
```json
{
  "needVar": true
}
```
this makes the command _require_ a parameter when called, useful when you don't want the
command called without a parameter

paramReplace
-
example:
```json
{
  "send": "parameter: {0}", 
  "paramReplace": "{0}" 
}
```
this replaces the given text ({0} in this case) with the parameter one's<br>

canBeUsedBy
-
example:
```json
{
  "canBeusedBy": "mod" 
}
```
this makes the command usable _only_ by the given value<br>
you can use as a value: everyone, mod, streamer

data
-
example:
```json
{
  "data": {}
}
```
in this object are placed data operations (ex. url) that manipulates external data

url
-
example:
```json
{
  "data": {
    "url": "https://something.com/textfile.txt"
  }
}
```
this will replace a {} in the send action with the text contained in the file pointed by the given URL

urljson
-
example:
```json
{
  "data": {
    "urljson": "https://something.com/jsonfile.json",
    "sections": ["text"]
  }
}
```
this will replace a {} with the value inside the last section given in the json file pointed by the URL<br>
(i know, this sounds difficult, but it is not)

sections
-
see urljson

load
-
example:
```json
{
  "data": {
    "load": "varname"
  }
}
```
replaces {var} with a previusly saved value (varname in this case)

saveAs
-
example:
```json
{
  "data": {
    "saveAs": ["varname", "url"]
  }
}
```
saves the parameter or the url data to the given variable (url data to varname in this case)
this is used with load

<br>


dictionary
-
string: a line of text<br>
char: a single character<br>
boolean: true or false<br>
object: a new { } encapsulated section<br>
ping: a username starting with @<br>
mention: same as above<br>
parameter: a string put after the command<br>
variable: same as above<br>
command: a line of text that makes the bot doing something<br>