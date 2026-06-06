from database.models import async_session, AdminReminds, AiToken, Tarifs, Reviews, Challenges, Users, WeeksTextsBer, WeeksTextsMom
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
import logging


async def add_days_and_weeks(time_zone_for_msc: int):
    """Добавление дней и недель"""
    logging.info('add_days_and_weeks')
    async with async_session() as session:
        users_data = await session.scalars(select(Users).where(Users.time_zone == time_zone_for_msc))
        if users_data:
            users_data = users_data.all()
            for user in users_data:
                user.week = (user.days + 1)//7
                user.days += 1
            await session.commit()
