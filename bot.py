import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MESSAGE = [
    'your meme was shit so i confiscated it',
    'what do you think this is? r/funny? get this shit outta here',
    'STOP! this is the meme police. you are under arrest for posting a shitty meme',
    'damn bro, you got the whole squad laughing 😐',
    '🚔🚔 WEE WOO WEE WOO WEE WOO 🚔🚔',
    '**shit posts** do not belong in **shitposts**'
]
TICKET_MESSAGE = '`🧾1 Bad Meme ticket has been issued `'
bot = commands.Bot(command_prefix='!')


@bot.listen()
async def on_ready():
    print(f'{bot.user} reporting for duty')


@bot.listen()
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author == bot.user:
        await channel.send('i\'m a bad bitch you can\'t kill me')
        return

    if str(payload.emoji) == '🚨':
        response = random.choice(MESSAGE)
        await channel.send(f'<@!{message.author.id}> {response}')
        await message.delete(delay=0.1)


bot.run(TOKEN)
