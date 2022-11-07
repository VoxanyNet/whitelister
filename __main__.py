import json

from rcon.source import Client
import discord
from discord.ext import tasks
import requests as r
from mcstatus import JavaServer

import embeds

# load the config file
with open("config.json", "r") as file:
    config = json.load(file)

SERVER_IP = config["server_ip"]
RCON_PASSWORD = config["rcon_password"]
BOT_TOKEN = config["token"]

# create bot object
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    update_status.start()

@bot.slash_command()
async def whitelist(ctx, username):

    # fetch uuid from mojang api
    resp = r.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

    # if an account with that username doesnt exist, we notify the user
    if resp.status_code == 204:
        error = embeds.UsernameDoesNotExist(username)

        await ctx.respond(embed=error)

        return

    # player uuid
    uuid = resp.json()["id"]

    # create rcon client and whitelist requested user
    with Client(SERVER_IP, 25575, passwd=RCON_PASSWORD) as client:
        response = client.run(f"whitelist add {username}")

    success = embeds.Success(username, icon=f"https://crafatar.com/avatars/{uuid}")

    #print(type(response))

    await ctx.respond(embed=success)

@tasks.loop(seconds=5)
async def update_status():
    
    # get the player count of the minecraft server
    player_count = JavaServer(SERVER_IP).status().players.online

    if player_count == 1:
        status_message = f"{player_count} player"

    else:
        status_message = f"{player_count} players"

    # change the status of the bot with the updated amount of players
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=status_message
        )
    )

bot.run(BOT_TOKEN)
