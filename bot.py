from command_handler import *
from admin_commands import *
from aiohttp import ClientSession

token = "bot_token"
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = Client(intents=intents)
prefix = getPrefix()
BANNED_WORDS = ["cheat", "spoofer", "dox", "hack", "mods", "spoofing", "ddos", "kys", "kill yourself", "nigger", "faggot"]
WEBHOOKS = { # ChannelID:WebHookURL
    "channel_id":"https://discordapp.com/api/webhooks/itswebhook",
    "channel_id2":"https://discordapp.com/api/webhooks/itswebhook2"
}
@client.event
async def on_ready():
    print(f'{client.user} Logged on.')
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
    msgText = str(message.content)
    found_bwords = []
    for word in msgText.split(" "):
        for bword in BANNED_WORDS:
            if bword in word.lower():
                found_bwords.append(word)
    if len(found_bwords) >=1 and str(message.channel.id) in WEBHOOKS:
        for word in found_bwords:
            msgText = msgText.replace(word, len(word)*"#")
        async with ClientSession() as session:
            webhook = discord.Webhook.from_url(WEBHOOKS[str(message.channel.id)], adapter=discord.AsyncWebhookAdapter(session))

            await webhook.send(content=msgText, username=message.author.name, avatar_url=message.author.avatar_url)
            await message.delete()
        return
# below are just examples 
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

#################
client.run(token)