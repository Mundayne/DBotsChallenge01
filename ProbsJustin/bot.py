#rewrite
#?gen [words/paragraphs/list] [int]
import discord
from discord.ext import commands
import random
import aiohttp
import json
import os
bot = commands.Bot(command_prefix='?')


def start():
    if not os.path.exists(f"./config.json"):
        print('Config not found, creating it.')
        with open('config.json', 'w+') as f:
            data = {"config": {"token": ""}}
            json.dump(data, f)

    with open('config.json', 'r') as f:
        data = json.load(f)
        if not data.get('config').get('token'):
            print('please enter your token in config.json, you will need to re-run this program, it will close...')
            os.system("pause")
        token = data.get('config').get('token')
        return token


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


phrasedict = {}


def populate_phrases(filename):
    if phrasedict:
        return
    with open(filename, 'r', encoding='utf-8') as f:
        phrases = f.read().splitlines()
        for phrase in phrases:
            phrasedict.setdefault(len(phrase.split(" ")), list()).append(phrase)


def get_text(amount):
    output = ""
    populate_phrases('scripts.txt')

    if amount in phrasedict.keys():
        picked = random.choice(phrasedict[amount])
        return picked

    while amount > 0:
        picked_len = random.choice([k for k in phrasedict.keys() if k <= amount])
        picked = random.choice(phrasedict[picked_len])
        output += picked
        amount -= picked_len
    return output


@bot.group()
async def gen(ctx):
    """generate random text, paragraphs or words."""
    if ctx.invoked_subcommand is None:
        await ctx.send('What do you want to generate? Paragraphs, lists or words?')


@gen.command()
async def words(ctx, length: str=None):
    """generate a length of random words."""
    if not length or not length.isdigit():
        await ctx.send('You need to provide the amount of words as an int.')
        return

    await ctx.message.add_reaction("\U00002705")

    run_generator = get_text(int(length))
    if len(run_generator) <= 1950:
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{get_text(int(length))}')
        await ctx.send(embed=e)
    else:
        content = await get_url(run_generator)
        if content != 'invalid':
            message = 'The reply would exceed discord message length limit, here is the '
            e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message} [hastebin]({content}).')
            await ctx.send(embed=e)
        else:
            message = 'The reply would exceed discord message length limit, and hastebins.'
            e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message}')
            await ctx.send(embed=e)


@gen.command()
async def paragraphs(ctx, length: str=None):
    """generate a length of random paragraphs."""
    if not length or not length.isdigit():
        await ctx.send('You need to provide the amount of paragraphs as an int.')
        return

    await ctx.message.add_reaction("\U00002705")

    response_list = []
    for i in range(0, int(length)):
        response_list.append(get_text(random.randint(100, 200)))

    counter = 0
    new_line = ''
    for item in response_list:
        new_line += f" paragraph: {counter} - {item} \n"
        counter += 1
    content = await get_url(new_line)
    if content != 'invalid':
        message = 'The reply would exceed discord message length limit, here is the '
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message} [hastebin]({content}).')
        await ctx.send(embed=e)
    else:
        message = 'The reply would exceed discord message length limit, and hastebins.'
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message}')
        await ctx.send(embed=e)


@gen.command(name='list')
async def _list(ctx, length: str=None):
    """generate a list of items by length"""
    if not length or not length.isdigit():
        await ctx.send('You need to provide the amount of paragraphs as an int.')
        return

    await ctx.message.add_reaction("\U00002705")
    response_list = []
    for i in range(0, int(length)):
        response_list.append(get_text(random.randint(4, 15)))

    new_line = ''
    for item in response_list:
        new_line += f'\U000025CF {item} \n'
    if len(new_line) <= 1020:
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{new_line}')
        await ctx.send(embed=e)

    elif len(new_line) >= 1021:
        content = await get_url(new_line)
        if content != 'invalid':
            message = 'The reply would exceed discord message length limit, here is the '
            e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message} [hastebin]({content}).')
            await ctx.send(embed=e)
        else:
            message = 'The reply would exceed discord message length limit, and hastebins.'
            e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message}')
            await ctx.send(embed=e)


async def get_url(content):
    async with bot.aiohttp.post('https://haste.discordbots.mundane.tk/documents', data=content.encode('utf-8')) as resp:
        if resp.status == 200:
            key = await resp.json()
            url = f'https://haste.discordbots.mundane.tk/{key["key"]}.txt'
            return url
        else:
            return 'invalid'



async def download_scripts():
    if not os.path.exists(f"./scripts.txt"):
        url = 'https://raw.githubusercontent.com/SobieskiCodes/DBotsChallenge01/master/ProbsJustin/scripts.txt'
        async with bot.aiohttp.get(url=url) as resp:
            filename = os.path.basename('scripts.txt')
            with open(filename, 'wb') as f_handle:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
            return await resp.release()
    else:
        return


async def create_aiohttp():
    bot.aiohttp = aiohttp.ClientSession()


bot.loop.create_task(create_aiohttp())
bot.loop.create_task(download_scripts())
bot.run(start())
