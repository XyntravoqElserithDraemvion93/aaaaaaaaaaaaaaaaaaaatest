import asyncio
import nextcord
from nextcord.ext import commands
from asyncio_throttle.throttler import Throttler

BOT_TOKEN = os.getenv('DISCORD_TOKEN')

if not BOT_TOKEN:
    print("トークン入れろ!")
    exit(1)
    
CHANNEL_ID = 1437414209636925543
INTERVAL_SECONDS = 3 * 60 * 60 + 20 * 60

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

throttler = Throttler(rate_limit=1, period=INTERVAL_SECONDS)

async def periodic_sender():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID) or await bot.fetch_channel(CHANNEL_ID)
    while not bot.is_closed():
        async with throttler:
            await channel.send("こんにちは")

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
