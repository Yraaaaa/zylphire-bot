import discord
import random
import os
import json
import asyncio
import wikipedia,os
from chatbot import Chat, register_call
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from datetime import datetime
from discord.utils import get


bot = commands.Bot(command_prefix = '~', case_insensitive = True, help_command = None)
bot.remove_command('ping')
bot.remove_command('help')
status = cycle(['PvP in Doom Arena.','PvP in Bludrut Brawl.', 'AQWorlds.'])

@register_call("whoIs")
def who_is(query,session_id="general"):
  try:
    return wikipedia.summary(query)
  except Exception:
    for new_query in wikipedia.search(query):
      try:
        return wikipedia.summary(new_query)
      except Exception:
            pass
  return "I don't know about " + query
template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbotTemplate", "chatbottemplate.template")
chat = Chat(template_file_path)





page1 = discord.Embed(title = 'Help Page: 1', description = 'Prefix: ~', colour = discord.Colour.blue())
page1.add_field(name = 'Commands:', value = " \n*ud* — Search definitions from Urban Dictionary [~ud (word)].\n \n*ping* — Displays your current ping. [~ping].\n \n*tarot* — Randomly chooses a card from tarots cards [~tarot].\n \n*charpage* — Display a Charpage of the player\n[~charpage|char (player)].\n \n*serverlist* — Displays all the AQW Servers and Players [~serverlist].\n \n**NOTE:** More commands will be added soon.", inline = True)
page1.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/784993989170167839/828171830308765736/AQWMember.png')

page2 = discord.Embed(title = 'Help Page:', description = 'Prefix: ~', colour = discord.Colour.blue())
page2.add_field(name = 'Commands:', value = " \n*info* — Displays an Information about the user's account\n[~info @user].\n \n*av* — Displays the user's Avatar [~av @user].\n \n*cat* — Displays a random photo of a cat [~cat|cats|neko].\n \n*inv* — Creates an Invite Link of Zylphire Guild Server [~inv|invite].\n \n*bored* - Tells the other members the you are bored. [~bored].\n \n**NOTE:** More commands will be added soon.", inline = True)
page2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/784993989170167839/828171830308765736/AQWMember.png')

page3 = discord.Embed(title = 'Help Page:', description = 'Prefix: ~', colour = discord.Colour.blue())
page3.add_field(name = 'Commands:', value = " \n*ban* — Bans the user [~ban @user].\n \n*kick* — Kicks the user [~kick @user].\n \n*clear* — Clears messages [~clear|cls|clr (no. of messages)].\n \n*unban* — Unbans the user [~unban user#id].\n \n*timedate* — Displays your exact current time&date [~timedate|td|time|date].\n \n**NOTE:** More commands will be added soon.", inline = True)
page3.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/784993989170167839/828171830308765736/AQWMember.png')

bot.help_pages = [page1, page2, page3]

@bot.command()
async def help(ctx, amount = 1):
  await ctx.channel.purge(limit = amount)
  buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
  current = 0

  bot.help_pages[current].set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  bot.help_pages[current].timestamp = datetime.utcnow()

  msg = await ctx.send(embed = bot.help_pages[current])

  for button in buttons:
      await msg.add_reaction(button)

  while True:
    try:
      reaction, user = await bot.wait_for('reaction_add', check = lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)

    except asyncio.TimeoutError:
      embed = bot.help_pages[current].set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
      embed.set_footer(text = 'Timed Out.')
      await msg.clear_reactions()

    else:
      previous_page = current

      if reaction.emoji == u"\u23EA":
        current = 0

      elif reaction.emoji == u"\u25C0":
        if current > 0:
          current -= 1

      elif reaction.emoji == u"\u25B6":
        if current < len(bot.help_pages)-1:
          current += 1

      elif reaction.emoji == u"\u23E9":
        current = len(bot.help_pages)-1

      for button in buttons:
        await msg.remove_reaction(button, ctx.author)

      if current != previous_page:
        bot.help_pages[current].title = f"Help Page {current+1}:"
        bot.help_pages[current].set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
        bot.help_pages[current].timestamp = datetime.utcnow()
        await msg.edit(embed = bot.help_pages[current])




@bot.event
async def on_ready():
  activity = discord.Activity(name = status)
  change_status.start()


@tasks.loop(seconds = 10)
async def change_status():
  await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type=discord.ActivityType.playing, name = next(status)))


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
      await member.ban(reason = reason)
      await ctx.send(f'Banned {member.mention}\nReason: {reason}.')

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
  await member.kick(reason = reason)
  await ctx.send(f'Kicked {member.mention}\nReason: {reason}.')

@bot.command()
async def info(ctx, member : discord.Member, amount = 1):
  await ctx.channel.purge(limit = amount)
  reg_date = member.created_at.strftime("%Y-%m-%d")
  joined = member.joined_at.strftime("%Y-%m-%d")
  embed = discord.Embed(
    title = f'Name: {member.name}',
    description = member.mention,
    colour = discord.Colour.blue()
  )


  embed.add_field(name ="Highest role:", value = member.top_role.mention, inline = False)
  embed.add_field(name = 'ID:', value = member.id , inline = False)
  embed.add_field(name = 'Date Registered:', value = reg_date, inline = True)
  embed.add_field(name ="Date Joined:", value = joined, inline = False)
  embed.set_thumbnail(url = member.avatar_url)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  embed.timestamp = datetime.utcnow()
  await ctx.send(embed = embed)

#TEST
@bot.command()
async def bored(ctx, amount = 1):
  await ctx.channel.purge(limit = amount)
  emoji = '<:Yeeeeeyyyy:789463946256056360>'
  embed = discord.Embed(
    title = 'BORED...',
    description = f"{ctx.author.name} is sooooooooooooooooooooooooooo **Bored**.\n \n@everyone, let's play somethin else shall we? {emoji}",
    colour = discord.Colour.blue()
  )

  embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/797831702596419604.png?v=1')
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  embed.timestamp = datetime.utcnow()
  await ctx.send(embed = embed)
#TEST



@bot.command()
@commands.has_permissions(administrator = False)
async def atavar(ctx, member : discord.Member, amount = 1):
  await ctx.channel.purge(limit = amount)
  emoji = '<:machodancer:798355672331845642>'
  gif_ = ''
  embed = discord.Embed(
    title = f"**AVATAR**",
    description = f"**{member.mention}'s Avatar: {emoji}**",
    colour = discord.Colour.blue()
  )
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/798355672331845642.png?v=1')
  embed.set_image(url = 'https://media.discordapp.net/attachments/784993989170167839/829599590008750100/Unknown.jpg')
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  embed.timestamp = datetime.utcnow()
  await ctx.send(embed = embed)



@bot.command(aliases = ['avatar'])
async def av(ctx, member : discord.Member, amount = 1):
  await ctx.channel.purge(limit = amount)
  embed = discord.Embed(
    title = f"**AVATAR**",
    description = f"**{member.mention}'s Avatar:**",
    colour = discord.Colour.blue()
  )
  
  embed.set_image(url = member.avatar_url)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  embed.timestamp = datetime.utcnow()
  await ctx.send(embed = embed)





@bot.event
async def on_message_delete(message):
    attachment = message.attachments[0] if message.attachments else None

    if attachment:
        print(f"[+] DELETED in {message.guild} | {message.channel}=> {message.author}: {message.content};{attachment.url}")
    else:
        print(f"[+] DELETED in {message.guild} | {message.channel}=> {message.author}: {message.content}")


@bot.event
async def on_message_edit(message, edit):
    attachment = message.attachments[0] if message.attachments else None
    if attachment:
        print(f"[+] EDITED in {message.guild} | {message.channel}=> {message.author}: {message.content};{attachment.url} to {edit.content}")
    else:
        print(f"[+] EDITED in {message.guild} | {message.channel}=> {message.author}: {message.content} to {edit.content}")






@bot.command(pass_context = True)
async def ai(ctx, *, message):
  result = chat.respond(message)
  if (len(result)<=2048):
      embed = discord.Embed(
        title = 'Zylphire AI',
        description = result,
        colour = discord.Colour.blue()
      )
      embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
      await ctx.send(embed = embed)
  else: 
    embedList = []
    n = 2048
    embedList = [result[i:1+n] for i in range(0, len(result), n)]
    for num, item in enumerate(embedList, start = 1):
      if (num == 1):
        embed = discord.Embed(
          title = 'Zylphire AI',
          description = item,
          colour = discord.Colour.blue()
        )
        embed.set_footer(text = "Page {}".format(num))
        await ctx.send(embed = embed)
      else:
        embed = discord.Embed(
          description = item,
          colour = discord.Colour.blue()
        )
        embed.set_footer(text = "Page {}".format(num))
        await ctx.send(embed = embed)



















#Load Cogs command.
@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')

#Unload Cogs command.
@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


bot.run('Nzk3Mjc2MTkxMTM1NDk4MjUw.X_kHUA.WMuoDmdDjG9TRCqlYL0oVxIFvzo')