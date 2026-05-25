from database.models import async_session, Users
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
import logging


async def check_user(user_id: int) -> bool:
    """Проверка наличия пользователя в бд"""
    logging.info('check_user')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        if user:
            return True
        else:
            return False











