from rcon.source import Client
import discord
import requests as r

import embeds

RCON_PASSWORD = "MovingDay2019"
BOT_TOKEN = "MTAzMzg1MzI4MDAyNTA1OTM0OQ.GV76Hf.5Axqj-fccErGrojJ97DCpT-kejvQSfHFYXL6js"

# create bot object
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

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
    with Client("voxany.net", 25575, passwd=RCON_PASSWORD) as client:
        response = client.run(f"whitelist add {username}")

    success = embeds.Success(username, icon=f"https://crafatar.com/avatars/{uuid}")

    #print(type(response))

    await ctx.respond(embed=success)

bot.run(BOT_TOKEN)
