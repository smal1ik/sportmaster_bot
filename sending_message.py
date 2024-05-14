import asyncio
from asyncio import sleep
import openpyxl
from app.utils.config import settings
from aiogram import Bot
from tqdm import tqdm
import psycopg2
import os

async def message(tg_ids=0):
    bot: Bot = Bot(token=settings.BOT_TOKEN)
    workbook = openpyxl.load_workbook('for_messages.xlsx')
    sheet = workbook.active
    connection = psycopg2.connect(user="postgres",
                                  password=os.getenv('postgres_pswd'),
                                  host="213.171.8.131",
                                  port="5432",
                                  database="bot")
    cursor = connection.cursor()
    for tg_id in tqdm(tg_ids):
        href = "https://sportmaster.onelink.me/wSOs?pid=tg_official&c=adults_newcollection&af_adset=15022024&af_channel=contest&is_retargeting=true&af_param_forwarding=false&af_dp=sportmaster%3A%2F%2Fcatalog%2Fnovaya-kollekciya_odezhda_obuv%2F%3Futm_source%3Dtg_official%26utm_medium%3Dcontest%26utm_campaign%3Dadults_newcollection%26utm_content%3D15022024&af_web_dp=https%3A%2F%2Fwww.sportmaster.ru%2Fcatalog%2Fnovaya-kollekciya_odezhda_obuv%2F%3Futm_source%3Dtg_official%26utm_medium%3Dcontest%26utm_campaign%3Dadults_newcollection%26utm_content%3D15022024"
        promo = sheet['A1'].value
        sheet.delete_rows(0)
        text = f"""Класс! Теперь осталось дождаться результатов и проверить, что твои друзья перешли по ссылкам. А пока держи небольшой подарок — уникальный промокод на скидку 20% на одежду, обувь и аксессуары в Спортмастере \U0001F64C\U0001F3FB\n
Скидка действует до 6 марта и суммируется с другими, но общая сумма скидки не должна превышать 50%. Также она не распространяется на товары c жёлтыми ценниками и товары из категорий «Лучшая цена», «Предложение недели», «Финальная цена» и «Товар дня».\n
Переходи в <a href="{href}">мобильное приложение</a>, закидывай обновки на весну в корзину и обязательно используй свой промокод \U0001F609\n
<b>{promo}</b>\n
Следи за обновлениями в @sportmasterofficial — уже 7 марта определим 5 победителей с помощью рандомайзера.
"""
        select_query = f"""UPDATE public.users set get_promocode = '{promo}', followed_link = true where tg_id={int(tg_id)};"""
        try:
            cursor.execute(select_query)
            connection.commit()
            await bot.send_message(tg_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
            await sleep(0.2)
        except:
            print(tg_id)
            continue
    await bot.session.close()
    if connection:
        cursor.close()
        connection.close()

workbook = openpyxl.load_workbook('Рассылка.xlsx')
sheet = workbook.active
tg_ids = [x[0] for x in list(sheet.values)]
asyncio.run(message(tg_ids))