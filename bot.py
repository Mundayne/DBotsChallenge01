import discord
from discord.ext import commands
import random
import aiohttp
bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def get_text(amount):
    output = ''
    with open('scripts.txt', 'r', encoding='utf-8') as f:
        phrases = f.read()
        phrases = phrases.split('\n')
        list_of_phrases = []
        for phrase in phrases:
            if len(phrase.split(' ')) == amount:
                list_of_phrases.append(phrase)

        if list_of_phrases != []:
            return random.choice(list_of_phrases)

    while amount != 0:
        valid = list(phrase for phrase in phrases if len(phrase.split(" ")) <= amount)
        picked = random.choice(valid)
        output += f'{picked} '
        amount -= len(picked.split(" "))
    return output


@bot.group()
async def gen(ctx):
    """generate random text, paragraphs or words."""
    if ctx.invoked_subcommand is None:
        await ctx.send('What do you want to generate? Paragraphs or words?')


@gen.command()
async def words(ctx, length: str=None):
    """generate a length of random words."""
    if not length or not length.isdigit():
        await ctx.send('You need to provide the amount of words as an int.')
        return

    run_generator = get_text(int(length))
    if len(run_generator) <= 1950:
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{get_text(int(length))}')
        await ctx.send(embed=e)
    else:
        content = await get_url(run_generator)
        message = 'The reply would exceed discord message length limit, here is the '
        e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message} [hastebin]({content}).')
        await ctx.send(embed=e)


@gen.command()
async def paragraphs(ctx, length: str=None):
    """generate a length of random paragraphs."""
    if not length or not length.isdigit():
        await ctx.send('You need to provide the amount of paragraphs as an int.')
        return

    response_list = []
    for i in range(0, int(length)):
        response_list.append(get_text(random.randint(100, 250)))

    counter = 0
    new_line = ''
    for item in response_list:
        new_line += f" paragraph: {counter} - {item} \n"
        counter += 1
    content = await get_url(new_line)
    message = 'The reply would exceed discord message length limit, here is the '
    e = discord.Embed(colour=discord.Colour(0x278d89), description=f'{message} [hastebin]({content}).')
    await ctx.send(embed=e)


async def get_url(content):
    async with bot.aiohttp.post('https://haste.discordbots.mundane.tk/documents', data=content.encode('utf-8')) as resp:
        key = await resp.json()
        url = f'https://haste.discordbots.mundane.tk/{key["key"]}.txt'
        return url


async def create_aiohttp():
    bot.aiohttp = aiohttp.ClientSession()

bot.loop.create_task(create_aiohttp())
bot.run('')
