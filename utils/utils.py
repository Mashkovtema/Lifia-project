import logging


async def process_time_settings(current_hour: int, current_minute: int, action: str, flag: str):
    """Настройка времени"""
    logging.info('process_time_settings')

    if action == 'up':
        if flag == 'hour':
            if current_hour == 23:
                current_hour = 0
            else:
                current_hour += 1
        if flag == 'minute':
            if current_minute == 55:
                current_hour += 1
                if current_hour > 23:
                    current_hour = 0
                current_minute = 0
            else:
                current_minute += 5
    else:
        if flag == 'hour':
            if current_hour == 0:
                current_hour = 23
            else:
                current_hour -= 1
        if flag == 'minute':
            if current_minute == 0:
                current_hour -= 1
                if current_hour < 0:
                    current_hour = 23
                current_minute = 55
            else:
                current_minute -= 5

    # Форматируем в строки с ведущим нулём
    return f"{current_hour:02d}", f"{current_minute:02d}"


async def add_sticker_to_category(category: str) -> str:
    """Добавление эмодзи к напоминанию"""
    logging.info('add_sticker_to_category')
    if category == 'Прием врача':
        return '🏥 Прием врача'

    if category == 'Анализы':
        return '📋 Анализы'

    if category == 'Купить что-то малышу':
        return '🛒 Купить что-то малышу'

    if category == 'Заказать подгузники':
        return '📦 Заказать подгузники'

    if category == 'Пить воду':
        return '💧 Пить воду'

    if category == 'Витамины':
        return '💊 Витамины'

    if category == 'Поесть':
        return '🍲 Поесть'

    if category == 'Прогулка':
        return '🚶 Прогулка'

    if category == 'Отдохнуть':
        return '😴 Отдохнуть'



