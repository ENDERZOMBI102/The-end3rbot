Custom Commands Docs
-
Custom Commands are a powerful feature of this bot, they can do almost anything, from
sending text to press a key on your keyboard.<br>
and they're simple as json! (hjson support coming soon)

for a description of the terms used in this document see [dictionary](#dictionary)<br>
to know the order of execution of the sections see [order of execution](#order-of-execution)<br>

|section|value|parent|depends on|
|-------|-----|------|----------|
|[send](#send)|string|none|none|
|[press](#press)|string/char|none|none|
|[varIsPing](#varIsPing)|boolean|none|parameter|
|[needVar](#needVar)|boolean|none|parameter|
|[paramReplace](#paramReplace)|string|none|send, parameter|
|[canBeUsedBy](#canBeUsedBy)|string|none|none|
|[help](#help)|string|none|none|
|[data](#data)|object|none|- - - - - - -|
|[url](#url)|string|data|send|
|[urljson](#urljson)|string|data|send, sections|
|[sections](#sections)|array(string)|data|urljson|
|[load](#load)|string|data|send|
|[saveAs](#saveAs)|array(string)|data|parameter|

send
-
example:
```json
{
  "send": "this is text"
}
```
this section holds the text that the command will send, it can have text substitution with {} and data actions<br>
avaiable substitutions:
 - {sender} replace with sender username
 - {para} replace with parameter
 - {var} see [load](#load)
 

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

canBeUsedBy
-
example:
```json
{
  "canBeusedBy": "mod" 
}
```
this makes the command usable _only_ by the given value<br>
you can use as a value: everyone, op, mod, streamer

help
-
example:
```json
{
  "help": "this is the help text" 
}
```
this is the text that is displayed in the cmds command for this cc

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
this will replace a {url} in the send action with the text contained in the file pointed by the given URL

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
this will replace a {json} with the value inside the last section given in the json file pointed by the URL<br>
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
variable: a saved value<br>
command: a line of text that makes the bot doing something<br>

order of execution
-
1) message recived
2) check if message starts with SYMBOL
3) check if command exists
4) command found in the channel's custom commands
5) pass custom commands to handler
6) start cc execution
7) canBeUsedBy checks
8) variable checks
9) send replaces
10) data operations
11) press
12) send text
13) stop execution

[go up](#Custom-Commands-Docs)
