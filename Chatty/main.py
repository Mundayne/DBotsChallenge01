import discord # rewrite
from discord.ext import commands
import asyncio
import json
import codecs
import random
from datetime import datetime

bot = commands.Bot(command_prefix='!')

# Load the config file
def config_load():
    with open('config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)

# Dict of latin words from latin wiktionary
def load_words():
    with codecs.open('loremIpsum.json', 'r', encoding='utf-8-sig') as doc:
        return json.load(doc)

# Create a simple list from the weirdly formatted dictionary, excluding non-alphabetic words
word_list = []
for lst in load_words()['*']:
    lst = lst['a']['*']
    for item in lst:
        word = item['title']
        if word.isalpha():
            word_list.append(word)

# Divide total number of words pseudo-randomly over number of paragraphs
def get_paragraph_lengths(paragraphs, words):
    lower = round(words/paragraphs/2) # minimum words per paragraph
    upper = round(words/paragraphs*2) # maximum words per paragraph
    lengths = random.sample(range(lower, upper), paragraphs)
    while sum(lengths) < words:
        lengths[random.randint(0, paragraphs-1)] += 1
    while sum(lengths) > words:
        lengths[random.randint(0, paragraphs-1)] -= 1
    return lengths

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print('-' * 10)

@bot.command(aliases=['lorem', 'ipsum', 'loremipsum'])
async def lipsum(ctx, words=0, paragraphs=1):
    '''
    Generate random Lorem Ipsum text.
    '''
    try:
        await ctx.channel.trigger_typing()
    except discord.Forbidden:
        return

    # Verify that both the number of words and paragraphs are positive
    if words < 1:
        await ctx.send(f'The number of words can only be positive.')
        return
    if paragraphs < 1:
        await ctx.send(f'The number of paragraphs can only be positive.')
        return

    # Initialize variables
    text = ''
    paragraph_lengths = get_paragraph_lengths(paragraphs, words)
    sentence_length = random.randint(10, 30)
    punctuation = [', ', ', ', ', ', '; ', ': '] # comma is 3x more common

    for p in range(0, paragraphs):
        paragraph_length = paragraph_lengths[p] # get length for this paragraph

        word_num = 0
        for w in range(0, paragraph_length):
            word = word_list[random.randint(0, len(word_list)-1)] # get random word
            word_num += 1 # position of word in sentence

            # if new sentence, start with upper case, and choose sentence length
            if word_num % sentence_length == 1:
                sentence_length = random.randint(10, 30)
                word_num = 1
                word = word[:1].upper() + word[1:]

            text += word

            # add punctuation and/or space
            if not w == paragraph_length-1:
                if word_num == sentence_length:
                    text += '. '
                elif not random.randint(0, 20):
                    text += punctuation[random.randint(0, len(punctuation)-1)]
                else:
                    text += ' '
            else:
                text += '.'

        # Add whitespace between paragraphs
        if not p == paragraphs-1:
            text += '\n\n'

    # Check if message length is OK
    if len(text) > 2048:
        await ctx.send(f'Generated text exceeds maximum characters for Discord message. Try using fewer words.')
        return

    # Create and send embed
    embed = discord.Embed(title='Lorem Ipsum', description=text, timestamp=datetime.utcnow())
    embed.set_author(name='Chatty', icon_url='https://i.imgur.com/hu3nR8o.png')
    embed.set_footer(text=f'{words} words, {paragraphs} paragraphs')
    await ctx.send(embed=embed)

if __name__ == '__main__':
    config = config_load()
    if not config['token']:
        print('Please enter your token in the config file.')
    else:
        bot.run(config['token'])
