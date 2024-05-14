from app.database.models import User, async_session
from sqlalchemy import select, BigInteger, update, delete


async def add_user(tg_id: BigInteger, first_name: str, username):
    """
    Функция добавляет пользователя в БД
    """
    async with async_session() as session:
        session.add(User(tg_id=tg_id, first_name=first_name, username=username))
        await session.commit()

async def get_user(tg_id: BigInteger):
    """
    Получаем пользователя по tg_id
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result

async def change_promocode(tg_id: int, promo):
    """
    Пользователь получил промокод
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        promo = str(promo)
        await session.execute(update(User).where(User.tg_id == tg_id).values(get_promocode=promo))
        await session.commit()

async def change_following(tg_id: int):
    """
    Пользователь получил промокод
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        await session.execute(update(User).where(User.tg_id == tg_id).values(followed_link=True))
        await session.commit()

async def change_subbed(tg_id: int):
    """
    Пользователь получил промокод
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        await session.execute(update(User).where(User.tg_id == tg_id).values(subbed=True))
        await session.commit()

async def incriment_referral(tg_id: int):
    """
    Инкриментируем счетчик пользователя
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        count = result.count + 1

        await session.execute(update(User).where(User.tg_id == tg_id).values(count=count))
        await session.commit()

        if count == 3:
            return True
        else:
            return False

async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result

# НЕ ЗАБЫТЬ УБРАТЬ!
async def clear_data():
    async with async_session() as session:
        await session.execute(delete(User))
        await session.commit()