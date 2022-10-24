import discord

class UsernameDoesNotExist(discord.Embed):
    def __init__(self, username):
        super().__init__(color=0xff0000)

        self.add_field(name="Error", value="An account with that username does not exist", inline=False)
        self.set_footer(text="Whitelister")

class Success(discord.Embed):
    def __init__(self, username, icon):
        super().__init__(color=0xffffff)

        self.set_thumbnail(url=icon)
        self.add_field(name="Success", value=f"{username} has been whitelisted", inline=False)
        self.set_footer(text="Whitelister")
