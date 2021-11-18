from Config.config import OWNER_ID
from discord.ext.commands.errors import NotOwner


def check_owner(ctx):
    if ctx.author.id not in OWNER_ID:
        raise NotOwner("You are not the owner of the bot.")
    return True
