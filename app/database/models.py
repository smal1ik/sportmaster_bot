from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from app.utils.config import settings
from app.utils.states import State

engine = create_async_engine(settings.POSTGRESQL, echo=False)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    followed_link: Mapped[bool] = mapped_column(default=False)  #Перешел ли по ссылке
    count_ref: Mapped[int] = mapped_column(default=0)  #Количество рефок
    get_promocode: Mapped[str] = mapped_column(default='None')  #Выдача промокода
    subbed: Mapped[bool] = mapped_column(default=False)   #Подписка


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)