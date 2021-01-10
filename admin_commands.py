from commands import *
admin_channels = ["656217194694180917", "786137381228249098"] # IDs of admin channels
news_channel_name = "news"


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

registerCommandHandler("news", sendToNews, desc='Sends news', syntax='<text>', restricted=admin_channels)

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
registerCommandHandler("randuser", sendToRandUser, desc='Sends text to a random user', syntax='<text>', restricted=admin_channels)

async def kickMember(cmd, channel, client, message, target="", *reason):
    reas = " ".join(reason)
    if target != "":
        uid= target.replace("<", "").replace("!", "").replace("@", "").replace(">", "")
        user = get(client.get_all_members(), id=uid)
        if user:
            try:
                await user.kick(reason=reas)
                await channel.send("Successfully kicked da boi")
            except Exception as e:
                 await channel.send("***Error:***  `"+str(e)+"`")
        else:
            await channel.send("***User not found.***")

registerCommandHandler("kick", kickMember, desc='Kicks a member', syntax='<@member> [reason]', restricted=admin_channels)

async def banMember(cmd, channel, client, message, target="", *reason):
    reas = " ".join(reason)
    if target != "":
        uid= target.replace("<", "").replace("!", "").replace("@", "").replace(">", "")
        user = get(client.get_all_members(), id=uid)
        if user:
            try:
                await user.ban(reason=reas)
                await channel.send("Successfully banned da boi")
            except Exception as e:
                 await channel.send("***Error:***  `"+str(e)+"`")
        else:
            await channel.send("***User not found.***")

registerCommandHandler("ban", banMember, desc='Bans a member', syntax='<@member> [reason]', restricted=admin_channels)