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
bot_channel = None
cache_channel = 'bot-cache'
delete_emoji = '🚨'
delete_threshold = 1
reward_emoji = '🏆'
reward_threshold = 1


async def is_bot_channel(ctx):
    return ctx.channel == bot_channel if bot_channel else True


@bot.listen()
async def on_ready():
    print(f'{bot.user} reporting for duty')


@bot.listen()
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    cache = discord.utils.get(message.guild.text_channels, name=cache_channel)
    reactions = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    is_channel = await is_bot_channel(message)
    if not is_channel:
        return

    # the bot won't delete it's own message
    if message.author == bot.user:
        await channel.send('i\'m a bad bitch you can\'t kill me')
        return

    # conditions for deletion were met
    if payload.emoji.name == delete_emoji and reactions.count >= delete_threshold:
        await handle_delete(channel, cache, message, reactions)

    # conditions for reward were met
    if payload.emoji.name == reward_emoji and reactions.count >= reward_threshold:
        await channel.send(f'now that\'s a spicy meme <@!{message.author.id}>')


# restricts the bot to a certain channel or removes restriction
@bot.command()
async def restrict(ctx, args=None):
    global bot_channel

    if args is None:
        if bot_channel:
            await ctx.send(f'currently bound to channel {bot_channel.mention} (to remove, `!restrict off`)')
        else:
            await ctx.send(f'not currently bound to a channel')
        return

    if args == ('off' or 'Off'):
        bot_channel = None
        await ctx.send(f'successfully removed channel restriction (to set again, `!restrict <channel-name>`)')
        return

    bot_channel = discord.utils.get(ctx.guild.text_channels, name=args)
    if bot_channel is None:
        await ctx.send(f'can\'t find channel with name \"{args}\"')
    else:
        await ctx.send(f'successfully bound to channel {bot_channel.mention}')


# easy test command that sends an emoji
@bot.command()
@commands.check(is_bot_channel)
async def uwu(ctx):
    await ctx.send('(◡ ω ◡)')


async def handle_delete(channel, cache, message, reactions):
    img_url = message.attachments[0].url if message.attachments else None
    response = random.choice(RESPONSES)

    # build list of users that voted
    voters = []
    for user in (await reactions.users().flatten()):
        voters.append(f'{user.name}#{user.discriminator}')

    # build embed message
    embed = discord.Embed()
    embed.colour = discord.Colour.dark_red()
    embed.description = message.content
    embed.set_author(name=message.author)
    embed.set_footer(text=f'{", ".join(voters)} thought this meme sucked')

    # add image
    if img_url:
        embed.set_image(url=img_url)

    # cache message with voters, send response to original channel
    await cache.send(embed=embed)
    await channel.send(f'<@!{message.author.id}> {response}')
    await message.delete(delay=0.1)


bot.run(TOKEN)
