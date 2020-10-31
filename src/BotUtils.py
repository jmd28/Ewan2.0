import os
import random
import discord

def random_file(path):
    return os.path.join(path, random.choice(os.listdir(path)))

async def dm(user, msg):
    if not user.dm_channel: await user.create_dm()
    await user.dm_channel.send(msg)

async def dm_file(user, path):
    await user.create_dm()
    await user.dm_channel.send(file=discord.File(path))



