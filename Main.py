# Imports
import discord
import tweepy
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands, tasks
import aiohttp
from pymongo import MongoClient
import os
# Utils
import Utils

#  Erstellen des Client für discord

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(
    command_prefix=Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "Prefix"),
    intents=intents,
    case_insensitive=True)

# Tweepy

auth = tweepy.OAuthHandler(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "TwitterSide", "API_Key"),
                           Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "TwitterSide", "API_SECRET_Key"))
auth.set_access_token(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "TwitterSide", "ACCESS_Token"),
                      Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "TwitterSide", "ACCESS_SECRET_Token"))

api = tweepy.API(auth)


# MongoDB Initialisierung / Benachrichtigung sobald der Bot Online.


@client.listen()
async def on_ready():
    client.connection_url = Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "MongoDB", "Connection")
    Base = str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "MongoDB", "Base"))
    Uccount = str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "MongoDB", "Uccount"))
    Config = str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "MongoDB", "Config"))
    status = int(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "Status", "ID"))
    Text = Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "Status", "Text")
    game = "Destiny 2" if Text is None else Text

    choiceStatus = discord.Status.online if status == 1 else discord.Status.do_not_disturb
    choiceActivity = discord.Activity(type=discord.ActivityType.playing,
                                      name=game) if status == 1 else discord.Activity(
        type=discord.ActivityType.watching, name="WARTUNGSARBEITEN")

    await client.change_presence(status=choiceStatus, activity=choiceActivity)
    client.mongo = MongoClient(str(client.connection_url))
    client.Uccount = client.mongo[Base][Uccount]
    client.Config = client.mongo[Base][Config]

    get_twitter.start()
    print(f'DATENBANK AKTIV\n<-->\nONLINE\n<-->\n{client.user}\n<-->\nTwitter API AKTIV\n<-->')


@tasks.loop(minutes=1)
async def get_twitter():
    tweetL = api.user_timeline(id=2431136251, tweet_mode="extended")
    Newest_Tweet_id_String = tweetL[0].id_str

    base_URL = f'https://www.twitter.com/BungieHelp/status/{Newest_Tweet_id_String}'

    Newest_Tweet_Time = tweetL[0].created_at

    data = client.Config.find_one({"_id": "TwitterAPI"})

    if data["Time"] == Newest_Tweet_Time:

        return

    else:

        client.Config.update_one({"_id": "TwitterAPI"}, {"$set": {"Time": Newest_Tweet_Time}})

        async with aiohttp.ClientSession() as session:
            url = Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "ClientWebhooks", "TwitterHook")
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

            message = f"{base_URL}"

            await webhook.send(content=message, username="@BungieHelp",
                               avatar_url=client.user.avatar_url)



# Laden der Erweiterungen


x = 0

for filename in os.listdir('Extensions'):
    client.load_extension(f'Extensions.{filename[:-3]}') if filename.endswith(".py") else None
    x += 1
print(f"<-->\nCogs geladen! Anzahl: {x}\n<-->")


# Starten des Client mit dem Token


def token_output():
    data = Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "ClientSide", "Token")
    return data


client.run(token_output())
