import asyncio
from importlib import reload

import discord
from discord.utils import find

import bot
from bot import emojis                    # hack, remove when done

from config import selfbotToken

client = discord.Client()
clientEmojis = None

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
@asyncio.coroutine
def on_message(message):
    if message.author == client.user and message.content.startswith(','):
        parts = message.content[1:].split(' ')
        command = parts[0]
        args = parts[1:]

        if command == 'reload':
            reload(bot)

        elif command in bot.selfCommands:
            print('Dispatching {}'.format(command))
            yield from bot.selfCommands[command](client, message, args)

client.run(selfbotToken, bot=False)
