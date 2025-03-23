import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks, commands
import os
from discord.utils import get

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}.')


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
intents.members = True  # Required for fetching member details
intents.presences = True  # If needed for user presence

import aiohttp
import asyncio

# | -- General Commands -- |

@client.command()
async def userinfo(ctx, user: discord.User = None):
    user = user or ctx.author  # Defaults to command author if no user is mentioned
    
    embed = discord.Embed(title="User Info", color=discord.Color.dark_red())
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="Username", value=f"{user.name}#{user.discriminator}", inline=False)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Creation", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Bot User", value="Yes" if user.bot else "No", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name} - Glory to Y76S.")
    
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.dark_red())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name} - Glory to Y76S.")
    
    await ctx.send(embed=embed)
# ------------------------------------------------------------------------------------------------

# | -- Events -- |

@client.event
async def on_member_join(member):
    #When a member joins the discord, they will get mentioned with this welcome message
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, welcome to the YS Public Affairs Server, make sure to read our guidelines in the designated channel.\n-# Glory to Y76S.')

@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Something seems to have happened, looks like you have missed out an argument for this command.\n-# Glory to Y76S.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Something seems to have happened, looks like you don't have the required permissions for this command.\n-# Glory to Y76S.")
    if isinstance(error, commands.MissingRole):
        await context.send("Something seems to have happened, looks like you don't have the required roles for this command.\n-# Glory to Y76S.")
    #bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Something seems to have happened, looks like I don't have the required permissions for this command.\n-# Glory to Y76S.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Something seems to have happened, looks like I don't have the required roles for this command.\n-# Glory to Y76S.")

# | -- Moderation Commands -- |
# | --   Prefix Commands   -- |

@client.command()
async def cmds(message):
    helpC = discord.Embed(title="Y76S Terminal \nCommands", description="Discord Bot manufactured by YS Laboratories.")
    helpC.add_field(name="purge", value="To use this command type ?purge and the number of messages you would like to delete, the default is 5.", inline=False)
    helpC.add_field(name="ban", value="To use this command, type ?ban and then mention the user you would like to perform this on.", inline=False)
    helpC.add_field(name="softban", value="To use this command, type ?softban and then mention the user you would like to perform this on.", inline=False)
    helpC.add_field(name="unban", value="To use this command, type ?unban and then type the username of the person you would like to perform this on.", inline=False)
    helpC.add_field(name="kick", value="To use this command, type ?kick and then type the username of the person you would like to perform this on.", inline=False)
    helpC.add_field(name="userinfo", value="To use this command, type ?userinfo and then type the username of the person you would like to perform this on.", inline=False)
    helpC.add_field(name="serverinfo", value="To use this command, type ?serverinfo and then type the username of the person you would like to perform this on.", inline=False)


    await message.channel.send(embed=helpC)

@client.command()
# | -- Checks whether the user has the correct permissions when this command is issued
@commands.has_permissions(manage_messages=True)
async def purge(context, amount=5):
    await context.channel.purge(limit=amount+1)

# | -- Kick and ban work in a similar way as they both require a member to kick/ban and a reason for this
@client.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'{member} has been kicked successfully.\n-# Glory to Y76S.')

@client.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} has been banned successfully.\n-# Glory to Y76S.')

# | -- Unbanning a member is done via typing ./unban and the ID of the banned member
@client.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await client.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} has been unbanned successfully.\n-# Glory to Y76S.')

# | -- Bans a member for a specific number of days
@client.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    # | -- multiplying the num of days the user enters by the num of seconds in a day
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} has been softbanned successfully.\n-# Glory to Y76S.')
    await asyncio.sleep(days)
    print("Time to unban")
    await member.unban()
    await context.send(f'{member} softban has finished.\n-# Glory to Y76S.')

client.run('PUT YOUR TOKEN HERE')
