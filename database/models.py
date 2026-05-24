from sqlalchemy import String, Integer, Boolean, BigInteger, MetaData, Table, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine("sqlite+aiosqlite:///database/database.sql")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class AdminReminds(Base):
    __tablename__ = 'AdminReminds'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String, default='---')
    time_type: Mapped[str] = mapped_column(String, default='---')
    times: Mapped[str] = mapped_column(String, default='---')
    days: Mapped[str] = mapped_column(String, default='---')
    users_type: Mapped[str] = mapped_column(String, default='---')
    comment: Mapped[str] = mapped_column(String, default='---')


class AiToken(Base):
    __tablename__ = 'AiToken'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String, default='---')


class Tarifs(Base):
    __tablename__ = 'Tarifs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tarif_type: Mapped[str] = mapped_column(String, default='---')
    name: Mapped[str] = mapped_column(String, default='---')
    cost: Mapped[int] = mapped_column(Integer, default=0)
    message_cnt: Mapped[int] = mapped_column(Integer, default=0)
    photo: Mapped[int]= mapped_column(String, default='---')


class Reviews(Base):
    __tablename__ = 'Reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, default=0)
    username: Mapped[str] = mapped_column(String, default='---')
    grade: Mapped[int] = mapped_column(Integer, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    moderation: Mapped[bool] = mapped_column(Boolean, default=False)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        review_1 = Reviews(
            user_id=24234234234,
            username='123123',
            grade=3,
            comment='Круто клсано'
        )
        review_2 = Reviews(
            user_id=24234234234,
            username='16666663',
            grade=5,
            comment='Круто'
        )
        review_3 = Reviews(
            user_id=24234234234,
            username='12312fggdfgsdgf3',
            grade=1,
            comment='Круто клсано fgdh fdghfdh'
        )
        review_4 = Reviews(
            user_id=24234234234,
            username='123123||',
            grade=2,
            comment=' клсано'
        )
        session.add(review_1)
        session.add(review_2)
        session.add(review_3)
        session.add(review_4)
        await session.commit()


