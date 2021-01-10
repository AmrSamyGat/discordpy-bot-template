# discordpy-bot-template
A discord bot with commands management system powered by discord.py

It uses a custom commands system to declare how commands work
to register a new command you can go to commands.py file
or make a new .py file, prepend `from commands import *` to it and import that file in bot.py file

# Usage:
```python
registerCommandHandler(cmd, handlerFunc, desc='No Description', syntax='', restricted=None)

#### Required parameters ####
# cmd is command name (string)
# handlerFunc is the returning function that gets called when you call the command (async function)
## handlerFunc arguments:
### handlerFunc(cmd, channel, client, message, *args) -> cmd is command name, channel is the current channel object, client is the bot client object, message is the current sent discord message object and *args are the inserted arguments in current called command

#### Optional parameters ####
# desc is the description of the command, a little explanation of what it does (string)
# syntax is the syntax of command usage, eg: "<Username>" (string)
## these are mostly used to show these info of the command when you call !help command

# restricted are the IDs of the only channels that the command should work in. (string when one channel, list of strings when several ones, set to None to work in all channels)
```
There are some default premade commands included with the source code like:
```js
/acc_age
/news
/ban
/kick
/randuser
/help
/addgame
/delgame
```
