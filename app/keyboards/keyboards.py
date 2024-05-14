from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

start_btn = InlineKeyboardBuilder()
start_btn.row(types.InlineKeyboardButton(
    text="Хочу!",
    callback_data="next")
)
start_btn = start_btn.as_markup()

rules_btn = InlineKeyboardBuilder()
rules_btn.row(types.InlineKeyboardButton(
    text="Да, подписка есть \U0001F44C\U0001F3FB",
    callback_data="check_sub")
)
rules_btn = rules_btn.as_markup()

subbed_btn = InlineKeyboardBuilder()
subbed_btn.row(types.InlineKeyboardButton(
    text="Хорошо",
    callback_data="first_task")
)
subbed_btn = subbed_btn.as_markup()

# в этих кнопках сделать отслеживание на переход
async def get_servs_btn(tg_id):
    servs_btn = InlineKeyboardBuilder()
    servs_btn.row(types.InlineKeyboardButton(
        text="Трекер активности",
        url=f"http://127.0.0.1:8000/url1/{tg_id}")
    )
    servs_btn.row(types.InlineKeyboardButton(
        text="Спортмастер Медиа",
        url=f"http://127.0.0.1:8000/url2/{tg_id}")
    )
    servs_btn.row(types.InlineKeyboardButton(
        text="Онлайн тренировки",
        url=f"http://127.0.0.1:8000/url3/{tg_id}")
    )
    servs_btn.row(types.InlineKeyboardButton(
        text="Афиша",
        url=f"http://127.0.0.1:8000/url4/{tg_id}")
    )
    servs_btn = servs_btn.as_markup()
    return servs_btn
