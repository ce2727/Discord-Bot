import discord
from discord.ext import commands

prefix = '!'

bot = commands.Bot(command_prefix=prefix)

#Data
IdDemerits = dict()
PrevChannel = dict()
JailedIdList = list()
ServerID = 309525231054094337
JailID = 381236419219161088

ServerName = "Grass Tastes Bad"
ModRoleName = "Mod"

Server = None
JailChannel = None



#Commands


#Login
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.id)
    #Set up variables
    for s in bot.servers:
        if s.name == ServerName:
            global Server
            Server = s
    for c in Server.channels:
        if c.name == "Jail":
            global JailChannel
            JailChannel = c


#Echo - replaces the user's command with the bot's echo of it
@bot.command(pass_context=True)
async def echo(ctx, *, message: str):
    await bot.delete_message(ctx.message)
    await bot.say(":mega: " + message)


#PrintDemerits - displays a user's demerits
@bot.command(pass_context=True)
async def printdemerits(ctx, *, member: discord.Member = None):
    if member == None:
        await bot.say(":x: User not found")
    else:
        if member.id in IdDemerits:
            #Create string list in print format
            demeritsPrintStr = ""
            for d in IdDemerits[member.id]:
                demeritsPrintStr += "-> " + d + "\n"


            embed = discord.Embed(
                title=member.name + "'s Demerits",
                color=0xe74c3c,
                description=demeritsPrintStr
            )
            #Send embeded list
            await bot.send_message(ctx.message.channel, embed=embed)
        else:
            await bot.say("User has no demerits!")

# ClearDemerits - clears a user's demerits
@bot.command(pass_context=True)
async def cleardemerits(ctx, *, member: discord.Member = None):
    if member is None:
        await bot.say(":x: User not found")
    else:
        if member.id in IdDemerits:
            del IdDemerits[member.id]
            await bot.say(member.name + "'s demerits have been cleared")
        else:
            await bot.say("User has no demerits!")

#Demerit - demerits a player
@bot.command(pass_context=True)
async def demerit(ctx, member: discord.Member, *args):
    reason = args[0]
    print("--------------------------------------")
    print("Demerit request issued by " + ctx.message.author.name + " for " + member.name)

    #Set member var
    #for m in server.members:#For each member
        #if m.name == strMember: #If that's their name
            #member = m #Assign member variable
            #found = True


    if member is not None:
        if (ModRoleName in [role.name for role in ctx.message.author.roles]):

            if member is None:
                print("Demerit issued on invalid user")
                await bot.say(ctx.message.author.mention + " I can't demerit the air! Specify a user.")
                return

            if member.id == "380886638286602241":#Bot ID
                print("Demerit on Bot blocked")
                await bot.say(ctx.message.author.mention + " Impossible, I'm perfect.")
                return

            #Demeriting admin
            elif (ModRoleName in [role.name for role in member.roles]):
                print("Demerit on administrator blocked")
                await bot.say(ctx.message.author.mention + " Boi, he's a Mod")
                return

            else: #Apply demerit
                #Check past demerits
                if member.id in IdDemerits.keys(): #If there is an entry
                    #Add a demerit
                    print("Adding demerit to " + member.name + "'s List")
                    IdDemerits[member.id].append(reason)
                    await bot.say(member.name + " Demerited :cop:")
                    #If it's 3 or more, take action
                    if len(IdDemerits[member.id]) >= 3:
                        print("Three demerits reached")
                        if member.id not in JailedIdList:
                            JailedIdList.append(member.id)  # Jail them
                            PrevChannel[member.id] = member.voice.voice_channel
                            await bot.move_member(member, JailChannel)
                            await bot.say(member.name + " Jailed for reaching 3 demerits :lock:")
                #If None, create with init val 1
                else:
                    print("Adding new demerit list for " + member.name)
                    await bot.say(member.name + " Demerited :cop:")
                    IdDemerits[member.id] = list()
                    IdDemerits[member.id].append(reason)
                return
    else:
        print("User not found")

#Forces user to say in jail voice channel until unjailed
@bot.command(pass_context=True)
async def jail(ctx, member: discord.Member = None):
    if (ModRoleName in [role.name for role in ctx.message.author.roles]):#If perms
        print("--------------------------------------")
        print("Jail request issued by " + ctx.message.author.name + " for " + member.name)
        if member is None:
            await bot.say(ctx.message.author.mention + ":x: User not found!")
            return

        if (member.id not in JailedIdList):#If they are a valid player and aren't already jailed
            JailedIdList.append(member.id)#Jail them
            PrevChannel[member.id] = member.voice.voice_channel
            await bot.move_member(member, JailChannel)
            await bot.say(member.name + " Jailed :lock:")
    else:
        await bot.say("You aren't allowed to do that, " + ctx.message.author.name)

#Unjails user
@bot.command(pass_context = True)
async def unjail(ctx, member: discord.Member = None):
    if member is not None:
        if (ModRoleName in [role.name for role in ctx.message.author.roles]):#If perms
            JailedIdList.remove(member.id)
            await bot.say(member.name + " Unjailed :unlock:")
            await bot.move_member(member, PrevChannel[member.id])
        else:
            await bot.say("You aren't allowed to do that, " + ctx.message.author.name)
    else:
        await bot.say(":x: User not found!")

#Fires every time a member changes channel
@bot.event
async def on_voice_state_update(before, after):
    if after.id in JailedIdList:
        if not(after.voice.voice_channel == JailChannel or after.voice.voice_channel == None):
            await bot.move_member(after, JailChannel)




bot.run('MzgwODg2NjM4Mjg2NjAyMjQx.DO_INg.lFEu5At_x45D_xqmcZe-FJwdRok')