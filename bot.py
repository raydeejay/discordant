import asyncio

import discord
from discord.utils import find

emojis = {
'a': ['🇦', '🅰'],
'b': ['🇧', '🅱'],
'c': ['🇨'],
'd': ['🇩'],
'e': ['🇪', '📧'],
'f': ['🇫', '<:f1:311821140681293824>'],
'g': ['🇬'],
'h': ['🇭'],
'i': ['🇮', 'ℹ'],
'j': ['🇯'],
'k': ['🇰'],
'l': ['🇱'],
'm': ['🇲', 'Ⓜ'],
'n': ['🇳'],
'o': ['🇴', '🅾', '⭕', '\U0001f441\u200d\U0001f5e8'],
'p': ['🇵', '🅿'],
'q': ['🇶'],
'r': ['🇷'],
's': ['🇸', '💲'],
't': ['🇹', '<:t1:311822462973247488>'],
'u': ['🇺'],
'v': ['🇻'],
'w': ['🇼'],
'x': ['🇽', '❌'],
'y': ['🇾'],
'z': ['🇿'],
}


# the mandatory `moo` command
@asyncio.coroutine
def moo(client, message, args):
    yield from client.delete_message(message)
    yield from client.send_message(message.channel, 'moo')


# general bot commands
@asyncio.coroutine
def helpx(client, message, args):
    yield from client.delete_message(message)
    yield from client.send_message(message.channel, '**Available commands**:\n```{}```'.format(', '.join(commands)))


# channel subscriptions
def get_sub_role(name, server):
    return find(lambda r: r.name == 'sub-{}'.format(name), server.roles)

@asyncio.coroutine
def subs(client, message, args):
    roles = [role.name[4:] for role in message.server.roles if role.name.startswith('sub-')]
    yield from client.delete_message(message)
    yield from client.send_message(message.channel, '**Available subscriptions**:\n```{}```'.format(', '.join(roles)))

@asyncio.coroutine
def sub(client, message, args):
    role = get_sub_role(args[0], message.server)
    yield from client.delete_message(message)
    if role:
        yield from client.add_roles(message.author, role)

@asyncio.coroutine
def unsub(client, message, args):
    role = get_sub_role(args[0], message.server)
    yield from client.delete_message(message)
    if role:
        yield from client.remove_roles(message.author, role)


# image posting commands
@asyncio.coroutine
def proc(client, message, args):
    yield from client.delete_message(message)
    yield from client.send_file(message.channel, 'images/procedure.png')

@asyncio.coroutine
def point(client, message, args):
    yield from client.delete_message(message)
    yield from client.send_file(message.channel, 'images/point.png')


# meme-like commands
@asyncio.coroutine
def pins(client, message, args):
    chan = discord.utils.get(message.server.channels, name='help')

    if chan:
        em = discord.Embed(title='"HALP tmodloader no work!!1"',
                               description='**FOR NOW**, tModLoader is not compatible with Terraria 1.3.5. There are instructions to downgrade Terraria to 1.3.4.4 (in order to install tModLoader 0.9.2.3) pinned :pushpin: in {}, for Windows and for Linux/Mac.'.format(chan.mention),
                               colour=0x3498db)
        em.set_author(name='Discordant', icon_url=client.user.default_avatar_url)

        yield from client.delete_message(message)
        yield from client.send_message(message.channel, embed=em)

@asyncio.coroutine
def wrong(client, message, args):
    yield from client.delete_message(message)
    yield from client.send_message(message.channel, '```{}: You\'re doing it completely wrong.```'.format(' '.join(args).upper()))


# message management
@asyncio.coroutine
def get_candidates(client, channel, author, args):
    try:
        count = int(args[0])
    except:
        count = None

    candidates = yield from client.logs_from(channel, limit=100)
    msgs = []
    for msg in candidates:
        if msg.author == author:
            msgs.append(msg)
    return count, msgs

@asyncio.coroutine
def delete_messages(client, messages, cmdMessage=None):
    if cmdMessage:
        yield from client.delete_message(cmdMessage)

    for msg in messages:
        yield from client.delete_message(msg)

@asyncio.coroutine
def pack(client, message, args):
    count, msgs = yield from get_candidates(client, message.channel, message.author, args)

    newLines = [msg.content for msg in msgs[count:0:-1]]
    yield from delete_messages(client, msgs[1:count], msgs[0])
    yield from client.edit_message(msgs[count], '\n'.join(newLines))

@asyncio.coroutine
def pull(client, message, args):
    count, msgs = yield from get_candidates(client, message.channel, message.author, args)

    newLines = [msg.content for msg in msgs[count:0:-1]]
    yield from delete_messages(client, msgs[2:count + 1], msgs[0])
    yield from client.edit_message(msgs[1], '\n'.join(newLines))

@asyncio.coroutine
def prune(client, message, args):
    count, msgs = yield from get_candidates(client, message.channel, message.author, args)

    yield from delete_messages(client, msgs[:count + 1])
    for msg in msgs[:count + 1]:
        yield from client.delete_message(msg)

@asyncio.coroutine
def react(client, message, args):
    msgs = yield from client.logs_from(message.channel, limit=2)
    msgs = list(msgs)
    msg = msgs[1]
    yield from client.delete_message(msgs[0])

    usedLetters = []
    emoji = None

    print("Emojing: {}".format(args))

    for piece in args:
        if piece[0] == '<':
            emoji = discord.utils.get(message.server.emojis, name=piece.split(':')[1])
            print('Using an emoji splitted string')
            yield from client.add_reaction(msg, emoji)
        elif all([letter in emojis for letter in piece.lower()]):
            for letter in piece.lower():
                print('Using letters')
                emojiList = [v for v in emojis[letter] if (v not in usedLetters)]
                if len(emojiList) > 0:
                    emoji = emojiList[0]
                    usedLetters.append(emoji)
                    if ':' in emoji:
                        yield from client.add_reaction(msg, discord.utils.get(message.server.emojis, name=emoji.split(':')[1]))
                    else:
                        yield from client.add_reaction(msg, emoji)
        else:
            yield from client.add_reaction(msg, piece)


# commands
commands = {
    'moo': moo,
    'sub': sub,
    'subs': subs,
    'unsub': unsub,
    'prune': prune,
    'wrong': wrong,
    'pins': pins,
    'proc': proc,
    'point': point,
    'help': helpx,
    }

selfCommands = {
    'pack': pack,
    'pull': pull,
    'react': react,
    }

print("Bot module loaded.")
