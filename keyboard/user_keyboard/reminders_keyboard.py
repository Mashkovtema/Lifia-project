from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

import calendar

MONTHS_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

WEEKDAYS_RU = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


async def main_remind_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Мои напоминания', callback_data='my-reminds-user')
    btn_2 = types.InlineKeyboardButton(text='🤍 Забота о себе', callback_data='select-remind-category-user_health')
    btn_3 = types.InlineKeyboardButton(text='📅 Важное', callback_data='select-remind-category-user_important')
    btn_4 = types.InlineKeyboardButton(text='➕ Свое напоминание', callback_data='select-remind-category-user_custom')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    return markup


async def health_category_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='💧 Пить воду', callback_data='type-reminder-user_Пить воду')
    btn_2 = types.InlineKeyboardButton(text='💊 Витамины', callback_data='type-reminder-user_Витамины')
    btn_3 = types.InlineKeyboardButton(text='🍲 Поесть', callback_data='type-reminder-user_Поесть')
    btn_4 = types.InlineKeyboardButton(text='🚶 Прогулка', callback_data='type-reminder-user_Прогулка')
    btn_5 = types.InlineKeyboardButton(text='😴 Отдохнуть', callback_data='type-reminder-user_Отдохнуть')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_main')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    markup.inline_keyboard.append([btn_back])
    return markup


async def important_category_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='🏥 Прием врача', callback_data='type-reminder-user_Прием врача')
    btn_2 = types.InlineKeyboardButton(text='📋 Анализы', callback_data='type-reminder-user_Анализы')
    btn_3 = types.InlineKeyboardButton(text='🛒 Купить что-то малышу',
                                       callback_data='type-reminder-user_Купить что-то малышу')
    btn_4 = types.InlineKeyboardButton(text='📦 Заказать подгузники',
                                       callback_data='type-reminder-user_Заказать подгузники')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_main')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_back])
    return markup


async def select_remind_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Интервальное напоминание', callback_data='select-time-type-reminder-user_interval')
    btn_2 = types.InlineKeyboardButton(text='Раз в день', callback_data='select-time-type-reminder-user_one')
    btn_3 = types.InlineKeyboardButton(text='Определенная дата', callback_data='select-time-type-reminder-user_date')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_category')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_back])
    return markup


async def select_remind_type_my_reminds():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Интервальное напоминание', callback_data='select-my-remind-user_interval')
    btn_2 = types.InlineKeyboardButton(text='Раз в день', callback_data='select-my-remind-user_one')
    btn_3 = types.InlineKeyboardButton(text='Определенная дата', callback_data='select-my-remind-user_date')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data=back_callback)
    markup.inline_keyboard.append([btn])
    return markup


async def select_days_to_remind(selected_days: list):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    days_dict = {
        "Понедельник": "Понедельник",
        "Вторник": "Вторник",
        "Среда": "Среда",
        "Четверг": "Четверг",
        "Пятница": "Пятница",
        "Суббота": "Суббота",
        "Воскресенье": "Воскресенье"
    }

    for day in selected_days:
        if day in days_dict:
            days_dict[day] += " ✅"

    btn_1 = types.InlineKeyboardButton(text=days_dict['Понедельник'],
                                       callback_data='add-day-to-remind-user_Понедельник')
    btn_2 = types.InlineKeyboardButton(text=days_dict['Вторник'], callback_data='add-day-to-remind-user_Вторник')
    btn_3 = types.InlineKeyboardButton(text=days_dict['Среда'], callback_data='add-day-to-remind-user_Среда')
    btn_4 = types.InlineKeyboardButton(text=days_dict['Четверг'], callback_data='add-day-to-remind-user_Четверг')
    btn_5 = types.InlineKeyboardButton(text=days_dict['Пятница'], callback_data='add-day-to-remind-user_Пятница')
    btn_6 = types.InlineKeyboardButton(text=days_dict['Суббота'], callback_data='add-day-to-remind-user_Суббота')
    btn_7 = types.InlineKeyboardButton(text=days_dict['Воскресенье'],
                                       callback_data='add-day-to-remind-user_Воскресенье')
    btn_8 = types.InlineKeyboardButton(text="Каждый день", callback_data='add-day-to-remind-user_all-days')
    btn_9 = types.InlineKeyboardButton(text="Далее", callback_data='go-to-select-time-remind-user')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_select-type')
    markup.inline_keyboard.append([btn_1, btn_2])
    markup.inline_keyboard.append([btn_3, btn_4])
    markup.inline_keyboard.append([btn_5, btn_6])
    markup.inline_keyboard.append([btn_7, btn_8])
    markup.inline_keyboard.append([btn_9])
    markup.inline_keyboard.append([btn_back])
    return markup


async def time_settings_interval(current_hour: str, current_minute: str, selected_mode: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_up_hour = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-interval_up_hour')
    btn_up_minute = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-interval_up_minute')
    btn_hour = types.InlineKeyboardButton(text=str(current_hour), callback_data='ignore')
    btn_minute = types.InlineKeyboardButton(text=str(current_minute), callback_data='ignore')
    btn_down_hour = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-user-remind-interval_down_hour')
    btn_down_minute = types.InlineKeyboardButton(text='⬇️',
                                                 callback_data='time-settings-user-remind-interval_down_minute')

    markup.inline_keyboard.append([btn_up_hour, btn_up_minute])
    markup.inline_keyboard.append([btn_hour, btn_minute])
    markup.inline_keyboard.append([btn_down_hour, btn_down_minute])

    btn_add = types.InlineKeyboardButton(text='Добавить', callback_data='add-time-interval-remind-user')
    markup.inline_keyboard.append([btn_add])

    if selected_mode != 'any-reminds-zero':
        btn_ready = types.InlineKeyboardButton(text='Готово', callback_data='go-to-save-remind-user-date')
        markup.inline_keyboard.append([btn_ready])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_interval-remind')
    markup.inline_keyboard.append([btn_back])

    return markup


async def time_settings_one(current_hour: str, current_minute: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_up_hour = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-one_up_hour')
    btn_up_minute = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-one_up_minute')
    btn_hour = types.InlineKeyboardButton(text=str(current_hour), callback_data='ignore')
    btn_minute = types.InlineKeyboardButton(text=str(current_minute), callback_data='ignore')
    btn_down_hour = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-user-remind-one_down_hour')
    btn_down_minute = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-user-remind-one_down_minute')

    markup.inline_keyboard.append([btn_up_hour, btn_up_minute])
    markup.inline_keyboard.append([btn_hour, btn_minute])
    markup.inline_keyboard.append([btn_down_hour, btn_down_minute])

    btn_add = types.InlineKeyboardButton(text='Готово', callback_data='go-to-save-remind-user-date')
    markup.inline_keyboard.append([btn_add])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_select-type')
    markup.inline_keyboard.append([btn_back])

    return markup


async def time_settings_date(current_hour: str, current_minute: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_up_hour = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-date_up_hour')
    btn_up_minute = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-user-remind-date_up_minute')
    btn_hour = types.InlineKeyboardButton(text=str(current_hour), callback_data='ignore')
    btn_minute = types.InlineKeyboardButton(text=str(current_minute), callback_data='ignore')
    btn_down_hour = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-user-remind-date_down_hour')
    btn_down_minute = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-user-remind-date_down_minute')

    markup.inline_keyboard.append([btn_up_hour, btn_up_minute])
    markup.inline_keyboard.append([btn_hour, btn_minute])
    markup.inline_keyboard.append([btn_down_hour, btn_down_minute])

    btn_add = types.InlineKeyboardButton(text='Готово', callback_data='go-to-save-remind-user-date')
    markup.inline_keyboard.append([btn_add])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_select-type')
    markup.inline_keyboard.append([btn_back])

    return markup


async def days_period_buttons(month: int, year: int):
    month_name = MONTHS_RU.get(month, f'Месяц {month}')
    first_day, days_cnt = calendar.monthrange(year, month)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=f'{month_name} {year}', callback_data='ignore')
    ])

    week_row = []
    for day in WEEKDAYS_RU:
        week_row.append(InlineKeyboardButton(text=day, callback_data='ignore'))
    keyboard.inline_keyboard.append(week_row)

    current_row = []

    for _ in range(first_day):
        current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))

    for day in range(1, days_cnt + 1):
        current_row.append(
            InlineKeyboardButton(text=str(day), callback_data=f'select-date-to-remind-user_{year}_{month}_{day}'))

        if len(current_row) == 7:
            keyboard.inline_keyboard.append(current_row)
            current_row = []

    if current_row:
        while len(current_row) < 7:
            current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))
        keyboard.inline_keyboard.append(current_row)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='<<<', callback_data=f'pagination-date-remind-user_{prev_month}_{prev_year}'),
        InlineKeyboardButton(text='>>>', callback_data=f'pagination-date-remind-user_{next_month}_{next_year}')
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_select-type')
    ])

    return keyboard


async def add_or_no_or_back_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='add-new-remind-user-question_yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='add-new-remind-user-question_no')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_get-comment')
    markup.inline_keyboard.append([btn_yes, btn_no])
    markup.inline_keyboard.append([btn_back])
    return markup


async def delete_reminds(data: list, page: int):
    item_cnt = 2  # Кол-во объектов в одном блоке

    if (page < len(data) / item_cnt) and page >= 0:  # Проверка, что страница не последняя

        if len(data) % item_cnt > 0:  # Кол-во страниц
            all_pages = int(len(data) / item_cnt) + 1
        else:
            all_pages = int(len(data) / item_cnt)

        markup = types.InlineKeyboardMarkup(inline_keyboard=[])
        if len(data) <= item_cnt:
            for obj in data:
                obj = obj.__dict__
                btn = types.InlineKeyboardButton(text=f'{obj["category"]} {obj["comment"][:20]}',callback_data=f'select-remind-delete-user_{obj["id"]}')
                markup.inline_keyboard.append([btn])
        else:
            for obj in data[item_cnt * page: (item_cnt * page) + item_cnt]:
                obj = obj.__dict__
                btn = types.InlineKeyboardButton(text=f'{obj["category"]} {obj["comment"][:20]}', callback_data=f'select-remind-delete-user__{obj["id"]}')
                markup.inline_keyboard.append([btn])

            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-remind-user_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'Стр. {page + 1}/{all_pages}', callback_data=f'---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-remind-user_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-reminds-user_catedory-delete', style='danger')
        markup.inline_keyboard.append([btn_back])

        return markup

    else:
        return None


async def delete_or_no_reminds(page: int):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='confirm-delete-remind')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data=f'pagination-remind-user_{page}')
    markup.inline_keyboard.append([btn_yes, btn_no])
    return markup


