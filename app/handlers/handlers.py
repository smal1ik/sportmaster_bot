from datetime import timedelta

from app.database.requests import *

from aiogram import types, F, Router, Bot
import app.keyboards.keyboards as kb
import app.utils.copies as txt
from aiogram.filters.command import Command

from app.utils.config import settings

from aiogram.fsm.context import FSMContext
from app.utils.states import Status
router_main = Router()

@router_main.message(Command("clear"))
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
    await clear_data()

@router_main.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(str(message.from_user.id))
    user = await get_user(message.from_user.id)
    if not user:
        await state.set_state(Status.start)
        await message.answer(txt.start_text, reply_markup=kb.start_btn)
        # если пользователя нет, добавляем в таблицу
        await add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)

        ref = message.text.split(' ')
        if len(ref) == 2:
            ref = ref[1]
            if ref.isnumeric():
                result = await incriment_referral(ref)
                if result:
                    if user.followed_link:
                        await bot.send_message(ref, txt.notify_all_done)
                    else:
                        await bot.send_message(ref, txt.notify_friends_done)

    else:
        if not user.subbed:
            await message.answer(txt.push_sub_task, reply_markup=kb.rules_btn, parse_mode='markdown')
        elif not user.followed_link:
            servs_btn = await kb.get_servs_btn(message.from_user.id)
            await message.answer(txt.second_task_text, reply_markup=servs_btn, parse_mode='markdown')
        elif int(user.count_ref) < 3:
            ref = await txt.get_push_friend_task(message.from_user.id)
            await message.answer(ref, parse_mode='markdown')
        if user.get_promocode != 'None':
            promo = user.get_promocode
            text = await txt.get_promo_text(promo)
            await message.answer(text[0])
    # Какая то логика если челик жмет старт с уже запущенным ботом
    #     if not user.subbed:
    #         await message.answer(txt.rules_text, reply_markup=kb.rules_btn, parse_mode='markdown')
    #     elif not user.followed_link:
    #         await message.answer(txt.)
    # if user.get_promocode:


@router_main.callback_query(F.data == "next", Status.start)
async def rules_st(callback: types.CallbackQuery):
    await callback.message.answer(txt.rules_text, reply_markup=kb.rules_btn, parse_mode='markdown')


@router_main.callback_query(F.data == "check_sub")
async def check_sub(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id=settings.CHAT_ID, user_id=callback.from_user.id)
    if user_channel_status.status != 'left':
        await state.set_state(Status.subbed)
        await change_subbed(callback.from_user.id)
        await callback.message.answer(await txt.get_first_task_text(callback.from_user.id), reply_markup=kb.subbed_btn, parse_mode='markdown')
    else:
        await callback.message.answer(txt.notsub, reply_markup=kb.rules_btn)


@router_main.callback_query(F.data == "first_task", Status.subbed)
async def second_task(callback: types.CallbackQuery):
    servs_btn = await kb.get_servs_btn(callback.from_user.id)
    await callback.message.answer(txt.second_task_text, reply_markup=servs_btn, parse_mode='markdown')


#Тут роутер сделать когда он переходит по ссылке (хз что там в ответ придёт, пока тестово сделаю чтобы на сообщение запускалось)
#Ещё сделать чтобы он сюда не мог попасть если уже получал промокод
@router_main.message(F.text == "test")
async def second_task_done(message: types.Message, state: FSMContext):
    await state.set_state(Status.promo)
    text = await txt.get_promo_text()
    await message.answer(text[0], parse_mode='markdown')


@router_main.message()
async def any_text(message: types.Message):
    await message.answer("Ой, кажется, бот не понимает! Попробуй нажать на одну из кнопок, а если это не помогло — напиши нам под конкурсным постом.")


