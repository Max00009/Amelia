import discord
from discord.ext import tasks,commands
import requests
from dotenv import load_dotenv
import os
import datetime
import asyncio

load_dotenv()


NEWSAPI_KEY=os.getenv("NEWSAPI_KEY")
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")
NEWS_CHANNEL_ID=os.getenv("NEWS_CHANNEL_ID")



#bot
intents=discord.Intents.default()
intents.messages=True
intents.message_content=True

bot=commands.Bot(command_prefix="!" ,intents=intents)

def fetch_news():
    url=f"https://newsapi.org/v2/everything?q=AI OR programming OR blockchain&language=en&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    response=requests.get(url)
    if response.status_code==200:
       articles=response.json().get("articles",[])
       return [
            f"**{article['title']}**\n {article['url']}" for article in articles[:5]
        ]
    else:
       return ["Failed...try again later..."]


@bot.event
async def on_ready():
      print (f"👩{bot.user.name} is active...")
      daily_news_update.start()
@bot.event
async def on_message(message):
      if message.author == bot.user:
         return
      await bot.process_commands(message)



@tasks.loop(hours=24)
async def daily_news_update():
      now=datetime.datetime.now()
      target_time=now.replace(hour=14, minute=5, second=0, microsecond=0)
      if now>target_time:
        target_time+=datetime.timedelta(days=1)
      wait_time=(target_time-now).total_seconds()
      await asyncio.sleep(wait_time)

      channel=bot.get_channel(NEWS_CHANNEL_ID)
      if channel:
         articles=fetch_news()
         message="**Daily News Update!📢**\n\n"+"\n\n".join(articles)
         await channel.send(message)
      else:
         print ("Channel not found...")



@bot.command()
async def news(ctx):
       await ctx.send("Fetching latest tech news...")
       articles=fetch_news()
       message="\n\n".join(articles)
       await ctx.send(message)



bot.run(DISCORD_TOKEN)


















