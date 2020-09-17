import logging
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
RESPONSES = [
    'your meme was shit so i confiscated it',
    'what do you think this is? r/funny? get this shit outta here',
    'STOP! this is the meme police. you are under arrest for posting a shitty meme',
    'damn bro, you got the whole squad laughing 😐',
    '🚔🚔 WEE WOO WEE WOO WEE WOO 🚔🚔',
    '**shit posts** do not belong in **shitposts**'
]
TICKET_MESSAGE = '`🧾1 Bad Meme ticket has been issued `'

bot = commands.Bot(command_prefix='!')
bot_channel = 'bot-goes-brrr'
delete_threshold = 1


@bot.listen()
async def on_ready():
    print(f'{bot.user} reporting for duty')


@bot.listen()
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    cache = discord.utils.get(message.guild.text_channels, name="bot-cache")
    reactions = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    if channel.name != bot_channel:
        return

    # the bot won't delete it's own message
    if message.author == bot.user:
        await channel.send('i\'m a bad bitch you can\'t kill me')
        return

    # conditions for deletion were met
    if payload.emoji.name == '🚨' and reactions.count == delete_threshold:
        response = random.choice(RESPONSES)
        img_url = message.attachments[0].url if message.attachments else None
        await cache_message(cache, message.author, message.content, img_url)
        await channel.send(f'<@!{message.author.id}> {response}')
        await message.delete(delay=0.1)


# restricts the bot to a certain channel
@bot.command()
async def restrict(ctx, args):
    global bot_channel
    channel = discord.utils.get(ctx.guild.text_channels, name=args)
    if channel is None:
        await ctx.send(f'can\'t find channel with name \"{args}\"')
    else:
        bot_channel = args
        await ctx.send(f'successfully bound to channel {channel.mention}')


# easy test command that sends an emoji
@bot.command()
async def uwu(ctx):
    if str(ctx.channel) != bot_channel:
        return
    await ctx.send('(◡ ω ◡)')


async def cache_message(channel, author, text=None, img=None):
    embed = discord.Embed()
    embed.colour = discord.Colour.dark_red()
    embed.set_author(name=author)
    embed.description = text

    if img:
        embed.set_image(url=img)

    await channel.send(embed=embed)


bot.run(TOKEN)
