from commands import *
import discord
token = "NzI4Mjk4Mzc0ODYzOTEzMDAw.Xv4Xhg.tj56weSmyRoqXLv8U9g_MAl-0dQ"
client = Client()
prefix = getPrefix()

@client.event
async def on_ready():
    print(f'{client.user} is there!')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="UwU"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(prefix):
        args = getCMDArgs(message.content)
        cmd = args[0]
        args.pop(0)
        await handleCommand(cmd, message.channel, client, message, *args)
        return 
@client.event
async def on_member_join(member):
    role = get(member.guild.roles, name="Knights")
    await member.add_roles(role)

async def changeSt(cmd, channel, client, message, online="online", act="playing", *status):
    stype = discord.ActivityType.playing
    if(act == "listening" or act == "l"):
        stype = discord.ActivityType.listening
    elif(act == "watching" or act == "w"):
        stype = discord.ActivityType.watching
    elif(act == "streaming" or act == "s"):
        stype = discord.ActivityType.streaming
    else: 
        stype = discord.ActivityType.playing
    scolor = discord.Status.online
    if(online == "dnd" or online == "donotdisturb" or online == "dontdisturb" or online == "do_not_disturb" or online == "d"):
        scolor = discord.Status.do_not_disturb
    elif(online == "idle" or online == "i"):
        scolor = discord.Status.idle
    elif(online == "invisible" or online == "invis"):
        scolor = discord.Status.invisible
    else: 
        scolor = discord.ActivityType.playing
    await client.change_presence(status=scolor, activity=discord.Activity(type=stype, name=" ".join(status)))
registerCommandHandler("status", changeSt, desc='Sets bot status', syntax='<status:online/dnd/idle/invis> <activity:listening/watching/playing> <status_text:whatever>', restricted={"656217194694180917", "786137381228249098"})
#await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Akeed Abyu ely 3aml el beat"))
#################
client.run(token)