from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
import locale

MONTHS_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

WEEKDAYS_RU = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


async def main_buttons():
    markup = types.ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    btn_1 = types.KeyboardButton(text='Напоминания ⏰')
    btn_2 = types.KeyboardButton(text='Ключ к ии моделям 🗝')
    btn_3 = types.KeyboardButton(text='Создать рассылку 🗝')
    btn_4 = types.KeyboardButton(text='Редактировать тарифы ⚙️')
    btn_5 = types.KeyboardButton(text='Выгрузка пользователей 👥')
    btn_6 = types.KeyboardButton(text='Обучение модели 🤖')
    btn_7 = types.KeyboardButton(text='Модерация отзывов ⭐️')
    btn_8 = types.KeyboardButton(text='Списки задач 📋')
    markup.keyboard.append([btn_1, btn_2])
    markup.keyboard.append([btn_3, btn_4])
    markup.keyboard.append([btn_5, btn_6])
    markup.keyboard.append([btn_7])
    markup.keyboard.append([btn_8])
    return markup


async def start_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='🌸 Старт', callback_data='go-to-get-name-start')
    markup.inline_keyboard.append([btn])
    return markup


async def select_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_mom = types.InlineKeyboardButton(text='Скоро стану мамой', callback_data='select-start-not-mom')
    btn_not_mom = types.InlineKeyboardButton(text='Я уже мама', callback_data='select-start-mom')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-start-user_name', style='danger')
    markup.inline_keyboard.append([btn_mom])
    markup.inline_keyboard.append([btn_not_mom])
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
        current_row.append(InlineKeyboardButton(text=str(day), callback_data=f'select-mom-start-date_{year}_{month}_{day}'))

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
        InlineKeyboardButton(text='<<<', callback_data=f'mom-start-date_{prev_month}_{prev_year}', style='primary'),
        InlineKeyboardButton(text='>>>', callback_data=f'mom-start-date_{next_month}_{next_year}', style='primary')
    ])

    # 5. Кнопка "Назад"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='back-start-user_type', style='danger')
    ])

    return keyboard











