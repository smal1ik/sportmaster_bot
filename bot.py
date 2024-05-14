import asyncio
import logging
import sys


from app.utils.config import settings
from aiogram import Bot, Dispatcher, types
from app.handlers.handlers import router_main
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{settings.URL_WEBHOOK}/webhook")
    types.WebAppInfo
async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    await bot.delete_webhook()
    dp = Dispatcher()
    dp.include_router(router_main)

    await dp.start_polling(bot, polling_timeout=100)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
        print("Bot start")
    except KeyboardInterrupt:
        print('Bot stop')
    except Exception as e:
        print(e)