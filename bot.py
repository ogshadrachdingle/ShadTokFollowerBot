import discord
from discord.ext import commands, tasks
from TikTokApi import TikTokApi
import os

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

TIKTOK_USERNAME = "ogshadrachdingle"  # Your TikTok username
GUILD_ID = 1239649470237638678        # Your actual Discord server ID
CHANNEL_ID = 1370080172778459137      # Your actual voice channel ID

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_follower_channel.start()

@bot.command()
async def followers(ctx, username: str = TIKTOK_USERNAME):
    try:
        with TikTokApi() as api:
            user = api.user(username=username)
            stats = user.info()["stats"]
            count = stats["followerCount"]
            await ctx.send(f"**{username}** has **{count:,}** followers on TikTok!")
    except Exception as e:
        await ctx.send("Error fetching TikTok data.")
        print(e)

@tasks.loop(minutes=10)
async def update_follower_channel():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    try:
        with TikTokApi() as api:
            user = api.user(username=TIKTOK_USERNAME)
            stats = user.info()["stats"]
            count = stats["followerCount"]
            await channel.edit(name=f"followers: {count:,}")
    except Exception as e:
        print(f"Error updating followers: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
