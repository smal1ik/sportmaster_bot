from datetime import timedelta
from app.database.requests import *
from app.utils.config import settings

import os

from arq import Retry
from aiogram import Bot

async def startup(ctx):
    ctx['bot'] = Bot(token=settings.BOT_TOKEN)

async def shutdown(ctx):
    await ctx['bot'].session.close()

async def remind_message(ctx, chat_id):
    users = await get_all_users()
    remind_msg = ''
    for user in users:
        user = user[0]
        if not user.subbed:
            remind_msg = """Проверь свою подписку на @sportmasterofficial и участвуй в конкурсе с крутыми призами \U0001F643"""
        elif user.count_ref < 3:
            remind_msg = f"""Твои друзья всё ещё не перешли по ссылке? \U0001F494 Напомни им, чтобы стать участником конкурса, а мы будем ждать \U0001F60C \nСсылка: https://t.me/sportmaster\_test\_bot?start={user.tg_id}"""
        elif not user.followed_link:
            remind_msg = """Ты в одном шаге от промокода на скидку — осталось выполнить последнее задание \U0001F64C\U0001F3FB"""
    if remind_msg:
        bot: Bot = ctx['bot']
        await bot.send_message(chat_id, remind_msg)


class workersettings:
    max_tries = 2
    redis_settings = settings.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    allow_abort_jobs = True
    functions = [remind_message,]