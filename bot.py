# bot.py
import asyncio
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = client.get_user(payload.user_id)

    if str(payload.emoji) == '🚨':
        if message.author != client.user:
            await message.delete()
            await channel.send('your post was shit so i deleted it')
        else:
            await channel.send('you think i\'m gonna delete my own shit? bitch i\'m the police')


client.run(TOKEN)
