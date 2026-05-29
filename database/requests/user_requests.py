from database.models import async_session, Users, Tarifs, WeeksTextsBer, WeeksTextsMom, Reviews
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


async def get_text_by_days_cnt(days_cnt: int, type: str) -> str:
    """Получение текста в зависимости от дня беременности"""
    logging.info('get_text_by_days_cnt')
    async with async_session() as session:
        if type == 'mom':
            text = await session.scalar(select(WeeksTextsMom.text).where(WeeksTextsMom.day == days_cnt))
            return text
        else:
            text = await session.scalar(select(WeeksTextsBer.text).where(WeeksTextsBer.day == days_cnt))
            return text


async def select_reviews_to_watch() -> list:
    """Получение отзывово для просмотра"""
    logging.info('select_reviews_to_watch')
    async with async_session() as session:
        reviews_data = await session.scalars(select(Reviews).where(Reviews.moderation == True))
        if reviews_data:
            reviews_data = reviews_data.all()
            return reviews_data[::-1]
        else:
            return []


async def check_user_review(user_id: int) -> bool:
    """Проверка на то, оставил ли пользователь отзыв"""
    logging.info('check_user_review')
    async with async_session() as session:
        check = await session.scalar(select(Reviews).where(Reviews.user_id == user_id))
        if check:
            return True
        else:
            return False


async def add_new_review(user_id: int, username: str, review_data: dict) -> None:
    """Добавление нового отзыва"""
    logging.info('add_new_review')
    async with async_session() as session:
        new_review = Reviews(
            user_id=user_id,
            username=username,
            grade=review_data['grade'],
            comment=review_data['comment']
        )
        session.add(new_review)
        await session.commit()



















