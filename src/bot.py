# bot.py
import os
import random
import subprocess
import csv

import discord
import pprint

from dotenv import load_dotenv

from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

from GoogleDownload import get_img_url
from sketch import draw_img
from BotUtils import random_file, dm

import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#TODO: disable points in test mode

# guild


intents = discord.Intents.all()
# client = discord.Client(intents=intents)

client = Bot(command_prefix='|', intents=intents)

members = {}

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild} (id: {guild.id})\n'
    )
    members = {member.name: member.id for member in guild.members}

    print(f'Guild Members:')
    pprint.pprint(guild.members)
    pprint.pprint(guild.emojis)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        'woeoeoeoeoeoeoeoeeee they ain\'t gonna know what hit \'em!'
    )

# start game -rounds=5
# round
# choose word
# picture
# wait until a message matches the word
# five rounds
# leaderboard

class Pictionary(commands.Cog, name="Fun and Games"):

    rounds_left: int = 0
    w: str
    hintTime: datetime.time = datetime.datetime.now() 
    indexOfWord: int = 1

    def in_progress(self):
        return self.rounds_left > 0


    @commands.command(help='get hint')
    async def hint(self, ctx):
        if ((datetime.datetime.now() - self.hintTime).seconds < 7):
            await ctx.send('Settle down cowperson!!')
        elif not self.in_progress():
            await ctx.send('A game isn\'t being played idiot.')
        else:  
            await ctx.send(f'hint: {self.w[0:self.indexOfWord]}')
            self.indexOfWord += 1
            self.hintTime = datetime.datetime.now()

    @commands.command(help='play pictionary')
    async def pictionary(self, ctx, rounds=5):

        if self.in_progress():
            await ctx.send('A game of pictionary is already in progress! Please try again later.')
            return

        await ctx.send(f'Starting a game of pictionary with {rounds} rounds')
        self.rounds_left = int(rounds)

        scores = {}
        with open("halloween.txt") as f:
            words = [x.strip() for x in f.readlines()]

        while self.in_progress():
            await ctx.send(f"~~                     ~~\n**Round {rounds-self.rounds_left+1}/{rounds}**\n~~                     ~~")
            self.w = random.choice(words)
            self.indexOfWord = 1
            words.remove(self.w)
            print(self.w)
            url = get_img_url(self.w+"clipart")
            path = draw_img(url)
            await ctx.send(file=discord.File(path))
            winner = (await client.wait_for('message', check=lambda m: self.w.lower()==m.content.lower() and m.author is not client.user)).author.name
            
            await ctx.send(f"{winner} won round")
            scores[winner] = scores.get(winner, 0) + 1
            self.rounds_left -= 1

        winners = [x for x,y in scores.items() if y==max(scores.values())]
        pprint.pprint(scores)
        await ctx.send('**Winner(s):**')
        for it in winners:
            await ctx.send(it)


@client.event
async def on_message(message):

    if all(x in  message.content.lower() for x in ["spam", "darren"]):
        print('spamming darren')
        guild = discord.utils.get(client.guilds, name=GUILD)
        # pprint(guild)
        dazza = discord.utils.get(guild.members, name='JouJo Simpstar')
        for _ in range(10): await dm(dazza, 'Darren')

    await client.process_commands(message)

client.add_cog(Pictionary(client))

client.run(TOKEN)
