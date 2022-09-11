import discord
from discord import *
from discord.utils import get
import json
prefix = "!"
commands = {}

def getPrefix():
    return prefix
def tocolor(r,g,b):
    return Colour.from_rgb(r,g,b)

def getEmbed(title="", desc="", items={}, r=255, g=255, b=255, footer=None):
    embed = Embed(title=title, description=desc, color=tocolor(r, g, b))
    for name, value in items.items():
        embed.add_field(name=name, value=value, inline=False)
    if footer != None:
        embed.set_footer(text=footer)
    return embed
async def sendEmbed(channel, title="", desc="", items={}, r=255, g=255, b=255, text="", footer=None):
    embed = getEmbed(title, desc, items, r, g, b, footer)
    return await channel.send(text, embed=embed)
async def raiseError(ch, title, text):
    await sendEmbed(ch, title or "Error", text, {}, 255, 0, 0)
def registerCommandHandler(cmd, handlerFunc, desc='No Description', syntax='', restricted=None, restrictedRoles=None):
    if cmd in commands:
        return
    cmdInfo = {}
    cmdInfo["name"] = cmd
    cmdInfo["function"] = handlerFunc
    cmdInfo["desc"] = desc
    cmdInfo["channels"] = restricted
    cmdInfo["roles"] = restrictedRoles
    cmdInfo["syntax"] = f'!{cmd} {syntax}' if syntax != '' else f'!{cmd}'
    commands[prefix+cmd] = cmdInfo
def isCommand(message):
    if message.startswith(prefix):
        if message.find(" "):
            args = message.split(" ")
            cmd = args[0]
        else:
            cmd = message
        if cmd[0] == prefix:
            if cmd in commands:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def getCMDArgs(cmd):
    if cmd.find(" "):
        args = cmd.split(" ")
    else:
        args = [cmd]
    return args
async def handleCommand(cmd, channel, client, message, *argss):
    args = getCMDArgs(cmd)
    cmd = args[0]
    if not isCommand(cmd):
        return
    func = commands[cmd]["function"]
    ch = commands[cmd]["channels"]
    found = True
    r = commands[cmd]["roles"]
    foundR = True
    if(isinstance(ch, str) or isinstance(ch, list)):
        found = False
        if(isinstance(ch, str)):
            if str(channel.id) == str(ch):
                found = True
        elif(isinstance(ch, list)):
            for i in ch:
                if str(channel.id) == str(i):
                    found = True
                    break
    if((isinstance(r, str) or isinstance(r, list)) and message.guild != None):
        foundR = False
        if(isinstance(r, str)):
            role = discord.utils.find(lambda rr: str(rr.id) == r, message.guild.roles)
            if role in message.author.roles:
                foundR = True
        elif(isinstance(r, list)):
            for i in r:
                role = discord.utils.find(lambda rr: str(rr.id) == i, message.guild.roles)
                if role in message.author.roles:
                    foundR = True
                    break
    args.pop(0)
    if(found == True and foundR == True):
        return await func(commands[cmd]["name"], channel, client, message, *argss)
    return

def loadJSONFile(path):
    with open(path, "r", encoding='utf-8') as jsonF:
        return json.load(jsonF)
def writeJSONFile(path, data):
    with open(path, "w", encoding='utf-8') as jsonF:
        return json.dump(data, jsonF)

# Commands ---------- examples 

async def myAccAge(cmd, channel, client, message, target="", *cargs):
    if target != "":
        uid= target.replace("<", "").replace("!", "").replace("@", "").replace(">", "")
        user = client.get_user(int(uid))
        if user:
            user_c = user.created_at
            await channel.send(target+"***'s account was created at:***  `"+str(user_c)+"`")
        else:
            user_c = message.author.created_at
            await channel.send("***Your account was created at:***  `"+str(user_c)+"`") 
    else:
        user_c = message.author.created_at
        await channel.send("***Your account was created at:***  `"+str(user_c)+"`")
registerCommandHandler("acc_age", myAccAge, desc="Gets your/someone's account creation date", syntax='[OPTIONAL: @user]')

async def handleCommands(cmd, channel, client, message, command=" ", *cargs):
    command = list(command)
    command[0] = '' if command[0] == "!" else command[0]
    command = ''.join(command)
    if command == " " or (command != " " and not isCommand("!"+command)):
        cmds = {}
        for Command, info in commands.items():
            _ch = "channels" in info.keys() and info["channels"] or None
            _found = True
            _r = "roles" in info.keys() and info["roles"] or None
            _foundR = True
            if(isinstance(_ch, str) or isinstance(_ch, list)):
                _found = False
                if(isinstance(_ch, str)):
                    if str(channel.id) == str(_ch):
                        _found = True
                elif(isinstance(_ch, list)):
                    for i in _ch:
                        if str(channel.id) == str(i):
                            _found = True
                            break
            if((isinstance(_r, str) or isinstance(_r, list)) and message.guild != None):
                _foundR = False
                if(isinstance(_r, str)):
                    _role = discord.utils.find(lambda rr: str(rr.id) == _r, message.guild.roles)
                    if _role in message.author.roles:
                        _foundR = True
                elif(isinstance(_r, list)):
                    for i in _r:
                        _role = discord.utils.find(lambda rr: str(rr.id) == i, message.guild.roles)
                        if _role in message.author.roles:
                            _foundR = True
                            break
            elif((not message.guild or message.guild == None) and (isinstance(_r, str) or isinstance(_r, list))):
                _foundR = False
            if(_found == True and _foundR == True):
                cmds[Command] = f'Description: {info["desc"]}\nSyntax: {info["syntax"]}'
        await sendEmbed(channel=channel, title="Server Commands", desc="A list of available server commands", items=cmds, r=255, g=100, b=100)
    else:
        cmdinfo = f'Description: {commands["!"+command]["desc"]}\nSyntax: {commands["!"+command]["syntax"]}'
        await sendEmbed(channel=channel, title="Server Command Info", desc="Info about: !"+command, items={f"!{command}": cmdinfo}, r=255, g=100, b=140)
registerCommandHandler("help", handleCommands, desc='Gets server commands list', syntax='[OPTIONAL: command name]')
registerCommandHandler("commands", handleCommands, desc='Gets server commands list', syntax='[OPTIONAL: command name]')

async def test():
    pass