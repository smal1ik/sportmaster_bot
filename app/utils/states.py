from aiogram.fsm.state import StatesGroup, State

class Status(StatesGroup):
    start = State()
    subbed = State()
    promo = State()