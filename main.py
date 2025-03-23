# | -- Quick note from 9q, not all current code will be put here, as I don't feel the need to give out complex systems I may or not have made for YS.

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
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=int("310f0f", 16))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name} - Glory to Y76S.")
    
    await ctx.send(embed=embed)


@client.command()
async def userinfo(ctx, user: discord.User = None):
    user = user or ctx.author  # Defaults to command author if no user is mentioned
    
    embed = discord.Embed(title="User Info", color=int("310f0f", 16))
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="Username", value=f"{user.name}#{user.discriminator}", inline=False)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Creation", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Bot User", value="Yes" if user.bot else "No", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name} - Glory to Y76S.")
    
    await ctx.send(embed=embed)
# ------------------------------------------------------------------------------------------------

# | -- Events -- |

@client.event
async def on_member_join(member):
    await member.create_dm()
     # | -- When a member joins the discord, they will get mentioned with this welcome message
    await member.dm_channel.send(f'Hello {member.name}, welcome to the YS Public Affairs Server, make sure to read our guidelines in the designated channel.\n-# Glory to Y76S.')

# | -- Moderation Commands -- |
# | --   Prefix Commands   -- |

@client.command()
async def cmds(ctx, color: str = "310f0f", footer_text: str = "Y76S Terminal - Glory to Y76S."):
    # Convert hex color string to an integer
    embed_color = int(color, 16) if color.startswith("#") else int(color, 16)

    helpC = discord.Embed(
        title="Y76S Terminal - Commands", 
        description="Discord Bot manufactured by YS Laboratories.",
        color=embed_color
    )
    
    helpC.add_field(name="purge", value="To use this command type `?purge <number>` to delete messages (default: 5).", inline=True)
    helpC.add_field(name="ban", value="To use this command, type `?ban @user`.", inline=True)
    helpC.add_field(name="softban", value="To use this command, type `?softban @user`.", inline=True)
    helpC.add_field(name="unban", value="To use this command, type `?unban <user-ID>`.", inline=True)
    helpC.add_field(name="kick", value="To use this command, type `?kick @user`.", inline=True)
    helpC.add_field(name="userinfo", value="To use this command, type `?userinfo @user`.", inline=True)
    helpC.add_field(name="serverinfo", value="To use this command, type\n`?serverinfo`.", inline=True)
    helpC.add_field(name="ping", value="To use this command, type `?ping`.", inline=True)
    helpC.add_field(name="role", value="To use this command, type `?role`.", inline=True)
    helpC.add_field(name="derole", value="To use this command, type `?derole`.", inline=True)

    # Set customizable footer text
    helpC.set_footer(text=footer_text)

    await ctx.send(embed=helpC)

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

@client.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await ctx.send(f"{member.name} already has the `{role.name}` role.")
    else:
        await member.add_roles(role)
        await ctx.send(f"`{role.name}` has been successfully added to {member.name}.")

@client.command()
@commands.has_permissions(manage_roles=True)
async def derole(ctx, member: discord.Member, role: discord.Role):
    if role not in member.roles:
        await ctx.send(f"{member.name} does not have the `{role.name}` role.")
    else:
        await member.remove_roles(role)
        await ctx.send(f"`{role.name}` has been removed from {member.name} successfully.")


client.run('PUT YOUR TOKEN HERE')
