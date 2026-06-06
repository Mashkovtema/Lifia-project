from sqlalchemy import String, Integer, Boolean, BigInteger, MetaData, Table, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine("sqlite+aiosqlite:///database/database.sql")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    username: Mapped[str] = mapped_column(String, default='---')
    name: Mapped[str] = mapped_column(String, default='---')
    week: Mapped[int] = mapped_column(Integer, default=1)
    days: Mapped[int] = mapped_column(Integer, default=1)
    bonus_cnt: Mapped[int] = mapped_column(Integer, default=0)
    mom_or_not: Mapped[bool] = mapped_column(Boolean, default=True)
    subscription_type: Mapped[str] = mapped_column(String, default='---') # pro/default
    subscription_date_end: Mapped[str] = mapped_column(String, default='---')
    time_zone: Mapped[int] = mapped_column(Integer, default=0) # Разница с Москвой


class WeeksTextsBer(Base):
    __tablename__ = 'WeeksTextsBer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[int] = mapped_column(Integer, default=1)
    text: Mapped[str] = mapped_column(String, default='---')


class WeeksTextsMom(Base):
    __tablename__ = 'WeeksTextsMom'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[int] = mapped_column(Integer, default=1)
    text: Mapped[str] = mapped_column(String, default='---')
    sovet: Mapped[str] = mapped_column(String, default='---')


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
    tarif_type: Mapped[str] = mapped_column(String, default='---') # standart/pro
    name: Mapped[str] = mapped_column(String, default='---')
    cost: Mapped[int] = mapped_column(Integer, default=0)
    message_cnt: Mapped[int] = mapped_column(Integer, default=0)
    photo: Mapped[int]= mapped_column(String, default='---')


class Reviews(Base):
    __tablename__ = 'Reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    username: Mapped[str] = mapped_column(String, default='---')
    grade: Mapped[int] = mapped_column(Integer, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    moderation: Mapped[bool] = mapped_column(Boolean, default=False)


class Challenges(Base):
    __tablename__ = 'Challenges'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String, default='---') # Для беременных/Для родивших
    name: Mapped[str] = mapped_column(String, default='---')
    bonus_cnt: Mapped[int] = mapped_column(Integer, default='---')
    week: Mapped[int] = mapped_column(Integer, default='---')


class UsersChallenges(Base):
    __tablename__ = 'UsersChallenges'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    task_id: Mapped[int] = mapped_column(BigInteger, default=0)


class Diary(Base):
    __tablename__ = 'Diary'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    week: Mapped[int] = mapped_column(Integer, default=0)
    photo: Mapped[str] = mapped_column(String, default='---')
    mood: Mapped[str] = mapped_column(String, default='---')
    good_point: Mapped[str] = mapped_column(String, default='---')
    bad_point: Mapped[str] = mapped_column(String, default='---')


class Payments(Base):
    __tablename__ = 'Payments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    cost: Mapped[int] = mapped_column(Integer, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    status: Mapped[str] = mapped_column(String, default='Не оплачен')


class UserRemindsIntervals(Base): # Интервальное напоминание
    __tablename__ = 'UserRemindsIntervals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    category: Mapped[str] = mapped_column(String, default='---')
    days: Mapped[str] = mapped_column(String, default='---')
    times: Mapped[str] = mapped_column(String, default='---')


class UserRemindsDate(Base): # Напоминание на определенную дату
    __tablename__ = 'UserRemindsDate'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    category: Mapped[str] = mapped_column(String, default='---')
    date: Mapped[str] = mapped_column(String, default='---')
    time: Mapped[str] = mapped_column(String, default='---')


class UserRemindsOneDay(Base): # Напоминание раз в день
    __tablename__ = 'UserRemindsOneDay'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, default=0)
    comment: Mapped[str] = mapped_column(String, default='---')
    category: Mapped[str] = mapped_column(String, default='---')
    time: Mapped[str] = mapped_column(String, default='---')


class Referal(Base):
    __tablename__ = 'Referal'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_inviter: Mapped[int] = mapped_column(BigInteger, default=0)
    user_id_invitee: Mapped[int] = mapped_column(BigInteger, default=0)




async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


