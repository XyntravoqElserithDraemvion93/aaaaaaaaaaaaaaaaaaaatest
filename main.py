import asyncio
import os
import sys
import nextcord
from nextcord.ext import commands
from asyncio_throttle.throttler import Throttler

CHANNEL_ID = 1437414209636925543
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

if not BOT_TOKEN:
    print("トークン入れろ!")
    sys.exit(1)

INTERVAL_SECONDS = 3 * 60 * 60 + 20 * 60 


intents = nextcord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

throttler = Throttler(rate_limit=1, period=INTERVAL_SECONDS)

async def periodic_sender():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:

            channel = bot.get_channel(CHANNEL_ID) or await bot.fetch_channel(CHANNEL_ID)
            await channel.send("こんにちは")  
        except nextcord.Forbidden:

            await asyncio.sleep(600)
            continue
        except Exception:

            await asyncio.sleep(60)
            continue

        await asyncio.sleep(INTERVAL_SECONDS)

bot.loop.create_task(periodic_sender())

if __name__ == "__main__":
    try:
        print("=== Discord Bot 起動中 ===")
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        print("Bot終了:")
        sys.stdout.flush()
        sys.exit(0)
