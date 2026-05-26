from database.models import async_session, Users, Tarifs
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
from datetime import datetime, timedelta
import logging


async def check_user(user_id: int) -> bool:
    """Проверка наличия пользователя в бд"""
    logging.info('check_user')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        if user:
            return user.__dict__
        else:
            return False


async def get_tarifs_data(flag: str) -> dict:
    """Получение данных о тарифе"""
    logging.info('get_tarifs_data')
    async with async_session() as session:
        # flag = standart/pro
        tarif_data = await session.scalar(select(Tarifs).where(Tarifs.tarif_type == flag))
        return tarif_data.__dict__


async def add_new_user(data: dict, user_id: int, username: str) -> None:
    """Добавление нового пользователя"""
    logging.info('add_new_user')
    async with async_session() as session:
        date_now = datetime.now()
        date_of_end = (date_now + timedelta(days=3)).strftime("%d.%m.%Y")

        new_user = Users(
            user_id=user_id,
            username=username,
            name=data['name'],
            week=data['week'],
            mom_or_not=data['mom_or_not'],
            subscription_type=data['subscription_type'],
            subscription_date_end=date_of_end,
            time_zone=data['time_zone']
        )
        session.add(new_user)
        await session.commit()






