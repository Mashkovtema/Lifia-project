from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

import calendar


MONTHS_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

WEEKDAYS_RU = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


async def settings_buttons(mom_or_not: bool):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Часовой пояс', callback_data='user-settings-change-time-zone')
    btn_2 = types.InlineKeyboardButton(text='Период', callback_data='user-settings-change-period')
    btn_3 = types.InlineKeyboardButton(text='Подписка', callback_data='user-settings-change-subscription')

    if mom_or_not:
        btn_4 = types.InlineKeyboardButton(text='Дата рождения малыша', callback_data='user-settings-change-date')
    else:
        btn_4 = types.InlineKeyboardButton(text='Дата последней менструации', callback_data='user-settings-change-date')

    btn_5 = types.InlineKeyboardButton(text='Пригласить друга', callback_data='referal-data-user')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    return markup


async def time_zone_buttons(user_time_zone: str):
    time_zone_dict = {
        -1: "🇷🇺 Калининградское время (UTC+2)",
        0: "🇷🇺 Московское время (UTC+3)",
        1: "🇷🇺 Самарское время (UTC+4)",
        2: "🇷🇺 Екатеринбургское время (UTC+5)",
        3: "🇷🇺 Омское время (UTC+6)",
        4: "🇷🇺 Красноярское время (UTC+7)",
        5: "🇷🇺 Иркутское время (UTC+8)",
        6: "🇷🇺 Якутское время (UTC+9)",
        7: "🇷🇺 Владивостокское время (UTC+10)",
        8: "🇷🇺 Магаданское время (UTC+11)",
        9: "🇷🇺 Камчатское время (UTC+12)"
    }
    time_zone_dict[user_time_zone] += ' ✅'


    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text=time_zone_dict[-1], callback_data='change_time_zone_MSK-1')
    btn_2 = types.InlineKeyboardButton(text=time_zone_dict[0], callback_data='change_time_zone_MSK+0')
    btn_3 = types.InlineKeyboardButton(text=time_zone_dict[1], callback_data='change_time_zone_MSK+1')
    btn_4 = types.InlineKeyboardButton(text=time_zone_dict[2], callback_data='change_time_zone_MSK+2')
    btn_5 = types.InlineKeyboardButton(text=time_zone_dict[3], callback_data='change_time_zone_MSK+3')
    btn_6 = types.InlineKeyboardButton(text=time_zone_dict[4], callback_data='change_time_zone_MSK+4')
    btn_7 = types.InlineKeyboardButton(text=time_zone_dict[5], callback_data='change_time_zone_MSK+5')
    btn_8 = types.InlineKeyboardButton(text=time_zone_dict[6], callback_data='change_time_zone_MSK+6')
    btn_9 = types.InlineKeyboardButton(text=time_zone_dict[7], callback_data='change_time_zone_MSK+7')
    btn_10 = types.InlineKeyboardButton(text=time_zone_dict[8], callback_data='change_time_zone_MSK+8')
    btn_11 = types.InlineKeyboardButton(text=time_zone_dict[9], callback_data='change_time_zone_MSK+9')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    markup.inline_keyboard.append([btn_6])
    markup.inline_keyboard.append([btn_7])
    markup.inline_keyboard.append([btn_8])
    markup.inline_keyboard.append([btn_9])
    markup.inline_keyboard.append([btn_10])
    markup.inline_keyboard.append([btn_11])
    markup.inline_keyboard.append([btn_back])
    return markup


async def days_buttons(month: int, year: int):
    month_name = MONTHS_RU.get(month, f'Месяц {month}')
    first_day, days_cnt = calendar.monthrange(year, month)

    # Создаём пустую клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # 1. Строка с месяцем и годом
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=f'{month_name} {year}', callback_data='ignore', style='success')
    ])

    # 2. Строка с днями недели
    week_row = []
    for day in WEEKDAYS_RU:
        week_row.append(InlineKeyboardButton(text=day, callback_data='ignore', style='primary'))
    keyboard.inline_keyboard.append(week_row)

    # 3. Календарная сетка
    # Массив для хранения кнопок текущей строки
    current_row = []

    # Добавляем пустые дни перед началом месяца
    for _ in range(first_day):
        current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))

    # Добавляем дни месяца
    for day in range(1, days_cnt + 1):
        current_row.append(InlineKeyboardButton(text=str(day), callback_data=f'edit-date-settings_{year}_{month}_{day}'))

        # Если строка заполнена (7 кнопок), добавляем её в клавиатуру
        if len(current_row) == 7:
            keyboard.inline_keyboard.append(current_row)
            current_row = []

    # Добавляем пустые дни в конце, если нужно
    if current_row:
        while len(current_row) < 7:
            current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))
        keyboard.inline_keyboard.append(current_row)

    # 4. Строка навигации (<<< и >>>)
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='<<<', callback_data=f'edit-mom-start-date_{prev_month}_{prev_year}', style='primary'),
        InlineKeyboardButton(text='>>>', callback_data=f'edit-mom-start-date_{next_month}_{next_year}', style='primary')
    ])

    # 5. Кнопка "Назад"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    ])

    return keyboard


async def edit_period_buttons(mom_or_not: bool):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    if mom_or_not:
        btn_1 = types.InlineKeyboardButton(text='Я уже родила ✅', callback_data='---')
        btn_2 = types.InlineKeyboardButton(text='Я еще не родила', callback_data='edit-mom-status_False')
    else:
        btn_1 = types.InlineKeyboardButton(text='Я уже родила', callback_data='edit-mom-status_True')
        btn_2 = types.InlineKeyboardButton(text='Я еще не родила ✅', callback_data='---')

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    markup.inline_keyboard.append([btn_1, btn_2])
    markup.inline_keyboard.append([btn_back])
    return markup


async def days_period_buttons(month: int, year: int):
    month_name = MONTHS_RU.get(month, f'Месяц {month}')
    first_day, days_cnt = calendar.monthrange(year, month)

    # Создаём пустую клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # 1. Строка с месяцем и годом
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=f'{month_name} {year}', callback_data='ignore', style='success')
    ])

    # 2. Строка с днями недели
    week_row = []
    for day in WEEKDAYS_RU:
        week_row.append(InlineKeyboardButton(text=day, callback_data='ignore', style='primary'))
    keyboard.inline_keyboard.append(week_row)

    # 3. Календарная сетка
    # Массив для хранения кнопок текущей строки
    current_row = []

    # Добавляем пустые дни перед началом месяца
    for _ in range(first_day):
        current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))

    # Добавляем дни месяца
    for day in range(1, days_cnt + 1):
        current_row.append(InlineKeyboardButton(text=str(day), callback_data=f'edit-period-date-settings_{year}_{month}_{day}'))

        # Если строка заполнена (7 кнопок), добавляем её в клавиатуру
        if len(current_row) == 7:
            keyboard.inline_keyboard.append(current_row)
            current_row = []

    # Добавляем пустые дни в конце, если нужно
    if current_row:
        while len(current_row) < 7:
            current_row.append(InlineKeyboardButton(text='...', callback_data='ignore'))
        keyboard.inline_keyboard.append(current_row)

    # 4. Строка навигации (<<< и >>>)
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='<<<', callback_data=f'edit-period-mom-start-date_{prev_month}_{prev_year}', style='primary'),
        InlineKeyboardButton(text='>>>', callback_data=f'edit-period-mom-start-date_{next_month}_{next_year}', style='primary')
    ])

    # 5. Кнопка "Назад"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    ])

    return keyboard


async def subscription_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Оплатить подписку', callback_data='user-go-to-pay')
    btn_2 = types.InlineKeyboardButton(text='Сменить тариф', callback_data='change-subscription-type')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_back])
    return markup


async def select_new_subscription_type(type: str, pro_tarif_name: str, default_tarif_name: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    if type == 'pro':
        btn_1 = types.InlineKeyboardButton(text=pro_tarif_name + " ✅", callback_data='---')
        btn_2 = types.InlineKeyboardButton(text=default_tarif_name, callback_data='select-new-tarif-type-user_default')

    else:
        btn_1 = types.InlineKeyboardButton(text=pro_tarif_name, callback_data='select-new-tarif-type-user_pro')
        btn_2 = types.InlineKeyboardButton(text=default_tarif_name + " ✅", callback_data='---')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_tarif-settings', style='danger')

    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_back])
    return markup


async def go_to_pay_or_back(url: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_pay = types.InlineKeyboardButton(text='Оплатить', url=url)
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_select-new-tarif', style='danger')
    markup.inline_keyboard.append([btn_pay])
    markup.inline_keyboard.append([btn_back])
    return markup


async def go_to_pay_or_back_main(url: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_pay = types.InlineKeyboardButton(text='Оплатить', url=url)
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    markup.inline_keyboard.append([btn_pay])
    markup.inline_keyboard.append([btn_back])
    return markup


async def back_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='settings-user-back_main', style='danger')
    markup.inline_keyboard.append([btn_back])
    return markup













