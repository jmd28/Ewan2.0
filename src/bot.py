# bot.py
import os
import random
import subprocess
import asyncio
import csv
import json

import discord
import aiohttp
from socket import timeout
import pprint

from dotenv import load_dotenv
from collections import Counter
from itertools import product
from dataclasses import dataclass
from enum import Enum

from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

from BotUtils import random_file, dm

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
        f'{guild.name} (id: {guild.id})\n'
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

    def in_progress(self):
        return self.rounds_left > 0

    @commands.command(help='play pictionary')
    async def pictionary(self, ctx, rounds=5):

        if self.in_progress():
            await ctx.send('A game of pictionary is already in progress! Please try again later.')
            return

        await ctx.send(f'Starting a game of pictionary with {rounds} rounds')
        self.rounds_left = int(rounds)

        while self.in_progress():
            await ctx.send(f"Round {rounds-self.rounds_left}/{rounds}")
            w = get_word()
            img = get_img(word)
            await ctx.send(file=discord.FILE(img))
            winner = await client.wait_for('message', check=lambda m: w==m.content.lower() and m.author is not client.user)
            await ctx.send(f"{winner} won round")
        

        # rps_channel = ctx.channel
        # player1 = ctx.message.author
        # await ctx.send(f'{player1.name} wants play rock paper scissors... who accepts their challenge? (respond "I do")')
        # reply = await client.wait_for('message', check=lambda m: "i do" in m.content.lower() and m.author is not client.user)
        # player2 = reply.author

        # # begin game
        # await ctx.send(f'{player2.name} has accepted {player1.name}\'s challenge!')
        # await player1.send('Rock Paper Scissors - make your move!')
        # await player2.send('Rock Paper Scissors - make your move!')

        # replies = {
        #     'rock': '<:ShrekBoulder:698296575558156348>'
        #     ,'paper': ':roll_of_paper:'
        #     ,'scissors': ':scissors:'
        # }

        # def check(m):
        #     # must not be a self msg
        #     if m.author == client.user:
        #         return False

        #     # must be a dm
        #     if m.guild is True:
        #         return False

        #     # must be from either player 1 or player 2
        #     if not any(m.author == it for it in [player1, player2]):
        #         return False

        #     # check move valid
        #     found_moves = [r for r in replies if r in m.content.lower()]
        #     if len(found_moves) != 1:
        #         #TODO: add some sort of handling for bad message
        #         # async def send_err_msg():
        #         #     resps = ', '.join(replies.keys())
        #         #     await m.author.send(f'please respond with one of {resps}')            
        #         return False

        #     return True

        # @dataclass
        # class Move:
        #     val: str
        #     player: discord.User

        #     def __init__(self, m: discord.Message):
        #         self.val = [r for r in replies if r in m.content.lower()][0]
        #         self.player = m.author

        # move1 = Move(await client.wait_for('message', check=check))
        # await move1.player.send(f'waiting for other player to make their choice...\nYou\'ll be notified of the result of this game in the channel: {rps_channel.name}')
        # move2 = Move(await client.wait_for('message', check=check))
        # await rps_channel.send(f'Result of rock paper scissors game between {player1.mention} and {player2.mention}:')

        # # cases for outcomes
        # # - draw
        # if move1.val == move2.val:
        #     await rps_channel.send(f'{move1.player.name}\'s {replies[move1.val]} was an equal match against {move2.player.name}\'s {replies[move2.val]}! Everyone\'s a winner')
        #     # scores[rps_respondent.name] = scores.setdefault(rps_respondent.name, 0) + 2
        #     # scores[rps_initiator.name] = scores.setdefault(rps_initiator.name, 0) + 2
        #     self.rps_inProgress = False
        #     return

        # # - cases for which move1 wins
        # if (move1.val == 'rock' and move2.val == 'scissors') or (move1.val == 'scissors' and move2.val == 'paper') or (move1.val == 'paper' and move2.val == 'rock'):
        #     winner = move1
        #     loser = move2

        # else:
        #     winner = move2
        #     loser = move1

        # await rps_channel.send(f'{replies[winner.val]} beats {replies[loser.val]}!\n{winner.player.name} wins!')

        # @dataclass
        # class Score:
        #     # player: str
        #     kills: int
        #     deaths: int
        #     kd: float

        #     def __init__(self, row):
        #         self.kills = int(row[1])
        #         self.deaths = int(row[2])

        # # update scores TODO: make win percentage not cumulative score
        # with open('scores.csv', mode='r+') as scores_file:
        #     r = csv.reader(scores_file)

        #     # scores maps a player name to a Score object
        #     scores = {row[0] : Score(row) for row in r if not r.line_num == 1}

        #     # update/initialise kills and deaths as needed
        #     scores[winner.player.name].kills = scores.setdefault(winner.player.name, Score(["N/A","0","0","0.0"])).kills + 1
        #     scores[loser.player.name].deaths = scores.setdefault(loser.player.name, Score(["N/A","0","0","0.0"])).deaths + 1

        #     # update KD ratio
        #     try:
        #         scores[winner.player.name].kd = scores[winner.player.name].kills / scores[winner.player.name].deaths
        #     except ZeroDivisionError:
        #         scores[winner.player.name].kd = 'NO_DEATHS'
        #     try:
        #         scores[loser.player.name].kd = scores[loser.player.name].kills / scores[loser.player.name].deaths
        #     except ZeroDivisionError:
        #         scores[loser.player.name].kd = 'NO_DEATHS'

        #     # write dict to file
        #     scores_file.seek(0)
        #     scores_file.truncate()
        #     scores_file.write("Name, Kills, Deaths, Ratio\n")
        #     for name in scores.keys():
        #         scores_file.write(f"{name}, {scores[name].kills}, {scores[name].deaths}, {scores[name].kd}\n")

        # self.rps_inProgress = False

    # @commands.command(help='displays the scores for rock paper scissors')
    # async def leaderboard(self, ctx):
        
    #     with open('scores.csv', mode='r') as scores_file:
    #         await ctx.send("".join([x for x in scores_file][1:]))



@client.command(help='force words to pour out')
async def say(ctx, channel, *text):

    msg = " ".join(text)
    guild = discord.utils.get(client.guilds, name=GUILD)
    text_channel = discord.utils.get(guild.text_channels, name=channel)
    # pprint.pprint(guild.text_channels)

    if not text_channel:
        return await ctx.send(f"{channel} {msg}")
    await text_channel.send(msg)

@client.command(help='it\'s past our bedtime')
async def well(ctx):
    channel = ctx.author.voice.channel
    for x in channel.members:
        await x.edit(voice_channel=None, reason='neet neet diddly eet')
    print(f'purged channel: {channel}')



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
