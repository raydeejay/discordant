import asyncio
from importlib import reload

import discord
from discord.utils import find

import bot

from config import botToken

# the client
client = discord.Client()

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
    if message.content.startswith(','):
        parts = message.content[1:].split(' ')
        command = parts[0]
        args = parts[1:]

        if command == 'reload':
            reload(bot)

        elif command in bot.commands:
            print('Dispatching {}'.format(command))
            yield from bot.commands[command](client, message, args)


client.run(botToken)
