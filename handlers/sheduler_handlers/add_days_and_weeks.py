import logging
from database.requests import sheduler_requests


async def add_days_and_weeks_func(time_zone_for_msc: int):
    """Добавление пользователям дней и недель"""
    logging.info(f'add_days_and_weeks_func - {time_zone_for_msc}')
    await sheduler_requests.add_days_and_weeks(time_zone_for_msc)
