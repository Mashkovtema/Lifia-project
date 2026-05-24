from database.models import async_session, AdminReminds, AiToken, Tarifs
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


async def update_ai_token(ai_token: str) -> None:
    """Обновление токена к моделям"""
    logging.info('update_ai_token')
    async with async_session() as session:
        token = await session.scalar(select(AiToken).where(AiToken.id == 1))
        if token:
            token.token = ai_token
            await session.commit()
        else:
            new_token = AiToken(
                token=ai_token
            )
            session.add(new_token)
            await session.commit()


async def get_token() -> str:
    """Получение токена"""
    logging.info('get_token')
    async with async_session() as session:
        token = await session.scalar(select(AiToken.token).where(AiToken.id == 1))
        if token:
            return token
        else:
            return 'Не установлен'


async def get_tarif_type(tarif_type: str):
    """Получение тарифа по типу"""
    logging.info('get_tarif_type')
    async with async_session() as session:
        tarif_data = await session.scalar(select(Tarifs).where(Tarifs.tarif_type == tarif_type))
        if tarif_data:
            return tarif_data.__dict__
        else:
            return None


async def add_new_tarif(tarif_type: str, name: str, message_cnt: int, photo: str, cost: int) -> None:
    """Добавление нового тарифа"""
    logging.info('add_new_tarif')
    async with async_session() as session:
        new_tarif = Tarifs(
            tarif_type=tarif_type,
            cost=cost,
            name=name,
            message_cnt=message_cnt,
            photo=photo
        )
        session.add(new_tarif)
        await session.commit()


async def update_tarif_data(tarif_type: str, parametr: str, value: str) -> None:
    """Обновление данных о тарифах"""
    logging.info('update_tarif_data')
    async with async_session() as session:
        tarif_data = await session.scalar(select(Tarifs).where(Tarifs.tarif_type == tarif_type))
        if parametr == 'name':
            tarif_data.name = value
        if parametr == 'cost':
            tarif_data.cost = value
        if parametr == 'message-cnt':
            tarif_data.message_cnt = value
        if parametr == 'photo':
            tarif_data.photo = value
        await session.commit()

















