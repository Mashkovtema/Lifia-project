from database.models import async_session, AdminReminds
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
import logging


async def add_new_admin_remind(category: str, time_type: str, times: str, days: str, comment: str, users_type: str) -> None:
    """Добавление нового напоминания админом"""
    logging.info('add_new_admin_remind')
    async with async_session() as session:
        new_remind = AdminReminds(
            category=category,
            time_type=time_type,
            times=times,
            days=days,
            users_type=users_type,
            comment=comment
        )
        session.add(new_remind)
        await session.commit()


async def get_reminds_by_type(users_type: str) -> list:
    """Получение списка напоминаний по типу пользователей"""
    logging.info('get_reminds_by_type')
    async with async_session() as session:
        data = await session.scalars(select(AdminReminds).where(AdminReminds.users_type == users_type))
        if data:
            return data.all()
        else:
            return []


async def get_remind_by_index(remind_index: int) -> dict:
    """Получение напоминания по индексу"""
    logging.info('get_remind_by_index')
    async with async_session() as session:
        remind = await session.scalar(select(AdminReminds).where(AdminReminds.id == remind_index))
        return remind.__dict__


async def delete_remind_by_index(remind_index: int) -> None:
    """Удаление напоминания по индексу"""
    logging.info('delete_remind_by_index')
    async with async_session() as session:
        remind = await session.scalar(select(AdminReminds).where(AdminReminds.id == remind_index))
        await session.delete(remind)
        await session.commit()



















