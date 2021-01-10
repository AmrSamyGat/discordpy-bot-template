import discord
from discord import *
from discord.utils import get
#import youtube_dl
import random
import re
prefix = "!"
commands = {}

def getPrefix():
    return prefix
def tocolor(r,g,b):
    return Colour.from_rgb(r,g,b)

async def sendEmbed(channel, title="", desc="", items={}, r=255, g=255, b=255):
    embed = Embed(title=title, description=desc, color=tocolor(r, g, b))
    for name, value in items.items():
        embed.add_field(name=name, value=value, inline=False)
    #embed.set_thumbnail(url="http://noxus.ga/assets/pfp.png")
    await channel.send(embed=embed)

def registerCommandHandler(cmd, handlerFunc, desc='No Description', syntax='', restricted=None):
    if cmd in commands:
        return
    cmdInfo = {}
    cmdInfo["name"] = cmd
    cmdInfo["function"] = handlerFunc
    cmdInfo["desc"] = desc
    cmdInfo["channels"] = restricted
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

def handleCommand(cmd, channel, client, message, *argss):
    args = getCMDArgs(cmd)
    cmd = args[0]
    if not isCommand(cmd):
        return
    func = commands[cmd]["function"]
    ch = commands[cmd]["channels"]
    found = True
    if(isinstance(ch, str) or isinstance(ch, list)):
        found = False
        if(isinstance(ch, str)):
            print(channel.id)
            print(ch)
            if str(channel.id) == str(ch):
                found = True
        elif(isinstance(ch, list)):
            for i in ch:
                if str(channel.id) == str(i):
                    found = True
                    break
    args.pop(0)
    if(found == True):
        return func(commands[cmd]["name"], channel, client, message, *argss)
    else:
        return

# Commands
async def sendToRandUser(cmd, channel, client, message, *cargs):
    text = " ".join(cargs)
    user = random.choice(channel.guild.members)
    
    userch = user.dm_channel
    if userch == None:
        userch = await user.create_dm()
    try:
        await userch.send(text)
        await channel.send("***sent:***  `"+text+"` to :point_right: ***"+str(user)+"***")
    except Exception as e:
        await channel.send("***Error:***  `"+str(e)+"`") 
registerCommandHandler("randuser", sendToRandUser, desc='Sends text to a random user', syntax='<text>')

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
            cmds[Command] = f'Description: {info["desc"]}\nSyntax: {info["syntax"]}'
        await sendEmbed(channel=channel, title="Server Commands", desc="A list of available server commands", items=cmds, r=255, g=100, b=100)
    else:
        cmdinfo = f'Description: {commands["!"+command]["desc"]}\nSyntax: {commands["!"+command]["syntax"]}'
        await sendEmbed(channel=channel, title="Server Command Info", desc="Info about: !"+command, items={f"!{command}": cmdinfo}, r=255, g=100, b=140)
registerCommandHandler("help", handleCommands, desc='Gets server commands list', syntax='[OPTIONAL: command name]')
registerCommandHandler("commands", handleCommands, desc='Gets server commands list', syntax='[OPTIONAL: command name]')

games = ["League of legends", "CSGO", "Valorant", "Brawlhalla", "Fortnite"]
games_ref = {
    "lol":"League of legends", 
    "league":"League of legends", 
    "league of legends":"League of legends", 
    "csgo":"CSGO", 
    "counter strike":"CSGO",
    "counter strike global offensive":"CSGO",
    "valorant":"Valorant",
    "brawl":"Brawlhalla",
    "brawlhalla":"Brawlhalla",
    "fortnite":"Fortnite"
}
async def addGame(cmd, channel, client, message, *cargs):
    roleName = " ".join(cargs)
    roleName = re.sub("\s\s+" , " ", roleName).strip().lower()
    user = message.author
    if roleName in games_ref:
        role = get(user.guild.roles, name=games_ref[roleName])
        if role != None:
            try:
                await user.add_roles(role)
                await channel.send(":white_check_mark: Game role `"+games_ref[roleName]+"` has been attached to you!")
            except Exception as e:
                await channel.send("***Error:***  `"+str(e)+"`") 
    else:
        await channel.send(":space_invader: :x: Invalid game role name!.. please select another from the list below")
        gamesHelp = {}
        for game in games:
            gameHelp = "**Keys:**"
            for key, value in games_ref.items():
                if value == game:
                    gameHelp += "\n"
                    gameHelp += key
            gamesHelp[game] = gameHelp
        await sendEmbed(channel=channel, title="Game Roles", desc="A list of available game rules names", items=gamesHelp, r=255, g=100, b=100)

registerCommandHandler("addgame", addGame, desc='Adds a game role to you', syntax='<game_role_name>')

async def removeGame(cmd, channel, client, message, *cargs):
    roleName = " ".join(cargs)
    roleName = re.sub("\s\s+" , " ", roleName).strip().lower()
    user = message.author
    if roleName in games_ref:
        role = get(user.guild.roles, name=games_ref[roleName])
        if role != None:
            try:
                await user.remove_roles(role)
                await channel.send(":white_check_mark: Game role `"+games_ref[roleName]+"` has been detached from you!")
            except Exception as e:
                await channel.send("***Error:***  `"+str(e)+"`") 
    else:
        await channel.send(":space_invader: :x: Invalid game role name!.. please select another from the list below")
        gamesHelp = {}
        for game in games:
            gameHelp = "**Keys:**"
            for key, value in games_ref.items():
                if value == game:
                    gameHelp += "\n"
                    gameHelp += key
            gamesHelp[game] = gameHelp
        await sendEmbed(channel=channel, title="Game Roles", desc="A list of available game rules names", items=gamesHelp, r=255, g=100, b=100)

registerCommandHandler("removegame", removeGame, desc='Removes a game role from you', syntax='<game_role_name>')
registerCommandHandler("delgame", removeGame, desc='Removes a game role from you', syntax='<game_role_name>')

async def sendToNews(cmd, channel, client, message, *cargs):
    text = " ".join(cargs)
    text = re.sub("\s\s+" , " ", text).strip().lower()
    ch = discord.utils.get(message.guild.text_channels, name="news")
    if ch != None:
        try:
            await ch.send("@everyone, "+text)
            await channel.send("Successfully sent your message")
        except Exception as e:
            await channel.send("***Error:***  `"+str(e)+"`") 

registerCommandHandler("news", sendToNews, desc='Sends news', syntax='<text>', restricted="656217194694180917")

async def kickMember(cmd, channel, client, message, target="", *reason):
    reas = " ".join(reason)
    if target != "":
        uid= target.replace("<", "").replace("!", "").replace("@", "").replace(">", "")
        await channel.send("***ID:***  `"+str(uid)+"`")
        user = get(client.get_all_members(), id=uid)
        await channel.send("***user:***  `"+str(user)+"`")
        if user:
            try:
                await user.kick(reason=reas)
                await channel.send("Successfully kicked da boi")
            except Exception as e:
                 await channel.send("***Error:***  `"+str(e)+"`")
        else:
            await channel.send("***User not found.***")

registerCommandHandler("kick", kickMember, desc='Kicks a member', syntax='<@member> [reason]', restricted={"656217194694180917", "786137381228249098"})