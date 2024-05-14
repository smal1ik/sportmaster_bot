from aiogram import Bot
from app.utils.config import settings

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database.requests import *
import app.utils.copies as txt

app = FastAPI()

bot = Bot(token=settings.BOT_TOKEN)

@app.get('/afisha/{tg_id}')
async def redir_afisha(tg_id):
    ...
    return RedirectResponse("https://www.sportmaster.ru/promo/39681312/?utm_source=tg_official&utm_medium=contest&utm_campaign=interes_tracker&utm_content=15022024")


@app.get('/media/{tg_id}')
async def redir_media(tg_id):
    user = await get_user(tg_id)
    if user.get_promocode == 'None':
        promo = await txt.get_promo_text()
        await change_following(tg_id)
        await change_promocode(tg_id, promo[1])
        await bot.send_message(tg_id, text=promo[0], parse_mode="HTML")
    return RedirectResponse("https://www.sportmaster.ru/media/?utm_source=tg_official&utm_medium=contest&utm_campaign=interes_media&utm_content=15022024")

@app.get('/url3/{tg_id}')
async def main3(tg_id):
    user = await get_user(tg_id)
    if user.get_promocode == 'None':
        promo = await txt.get_promo_text()
        await change_following(tg_id)
        await change_promocode(tg_id, promo[1])
        await bot.send_message(tg_id, text=promo[0], parse_mode="HTML")
    return RedirectResponse("https://www.sportmaster.ru/media/workout/online-training/?utm_source=tg_official&utm_medium=contest&utm_campaign=interes_trenirovki&utm_content=15022024")

@app.get('/url4/{tg_id}')
async def main4(tg_id):
    user = await get_user(tg_id)
    if user.get_promocode == 'None':
        promo = await txt.get_promo_text()
        await change_following(tg_id)
        await change_promocode(tg_id, promo[1])
        await bot.send_message(tg_id, text=promo[0], parse_mode="HTML")
    return RedirectResponse("https://www.sportmaster.ru/afisha/?utm_source=tg_official&utm_medium=contest&utm_campaign=interes_afisha&utm_content=15022024")

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0')