import discord
from discord.ext import commands
from TikTokApi import TikTokApi
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def followers(ctx, username: str):
    try:
        with TikTokApi() as api:
            user = api.user(username=username)
            stats = user.info()["stats"]
            count = stats["followerCount"]
            await ctx.send(f"**{username}** has **{count:,}** followers on TikTok!")
    except Exception as e:
        await ctx.send("Error fetching TikTok data.")
        print(e)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
