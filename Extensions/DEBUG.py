# Import
from discord.ext import commands
import discord
import yaml
import pymongo
import aiohttp
import tweepy
# Utils
import Utils

# Cog Initialising


class DEBUG(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.group(invoke_without_command=True)
    async def debug(self, ctx):
        embed = discord.Embed(
            title="-<DEBUG>-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue),
            description="Dies ist der DEBUG - Modus. Es gibt 4 verschiedene Modes:"
                        "\n`!debug bool` - Setzt das Bool-Argument deines Uccounts zurück"
                        "\n`!debug ticket` - Löscht ein vorhandenes Ticket, wenn die Reaktion dafür nicht funktioniert"
                        "\n**Administration:** `!debug latency` - Zeigt die Latenz."
                        "\n**Administration:** `!debug version` - Versions kontrolle."
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 15)


    @debug.command()
    async def bool(self, ctx):

        Utils.DBPreconditioning.POST_Uccount(self, ctx.author)

        embed = discord.Embed(
            title="-<DEBUG>-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue),
            description="**DEBUG - Modus:** ```py\nbool - Argument auf False gestellt```"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 8)


    @debug.command()
    async def ticket(self, ctx):
        try:
            await Utils.DBPreconditioning.DEL_Ticket(self, ctx.author)
        except:
            pass

        embed = discord.Embed(
            title="-<DEBUG>-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue),
            description='**DEBUG - Modus:** ```py\ntype.Ticket({"_id": "'f'{ctx.author.id}''"}) - gelöscht```'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 8)


    @debug.command()
    @commands.is_owner()
    async def latency(self, ctx):

        embed = discord.Embed(
            title="-<DEBUG>-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue),
            description=f'**DEBUG - Modus:** ```py\nself.client.latency - {round((self.client.latency * 1000), 2)} ms```'
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 8)

    @debug.command()
    @commands.is_owner()
    async def version(self, ctx):

        embed = discord.Embed(
            title="-<DEBUG>-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue)
        )
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="PyYaml", value=f"{yaml.__version__}")
        embed.add_field(name="PyMongo", value=f"{pymongo.__version__}")
        embed.add_field(name="Aiohttp", value=f"{aiohttp.__version__}")
        embed.add_field(name="Tweepy", value=f"{tweepy.__version__}")

        await Utils.TimeSend.se_ctx(ctx, embed, 8)


# Cog Finishing


def setup(client):
    client.add_cog(DEBUG(client))
