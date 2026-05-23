from aiogram import types


async def select_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Для беременных', callback_data='select-remind-type-admin_Для беременных')
    btn_2 = types.InlineKeyboardButton(text='Для родивших', callback_data='select-remind-type-admin_Для родивших')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    return markup


async def add_delete_or_back():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Добавить ➕', callback_data='select-action-reminders-admin_add')
    btn_2 = types.InlineKeyboardButton(text='Удалить ➖', callback_data='select-action-reminders-admin_delete')
    btn_3 = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_select-type', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn])
    return markup


async def select_category():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='🏥 Прием врача', callback_data='category-reminder-admin_Прием врача')
    btn_2 = types.InlineKeyboardButton(text='📋 Анализы', callback_data='category-reminder-admin_Анализы')
    btn_3 = types.InlineKeyboardButton(text='🛒 Купить что-то малышу', callback_data='category-reminder-admin_Купить что-то малышу')
    btn_4 = types.InlineKeyboardButton(text='📦 Заказать подгузники', callback_data='category-reminder-admin_Заказать подгузники')
    btn_5 = types.InlineKeyboardButton(text='💧 Пить воду', callback_data='category-reminder-admin_Пить воду')
    btn_6 = types.InlineKeyboardButton(text='💊 Витамины', callback_data='category-reminder-admin_Витамины')
    btn_7 = types.InlineKeyboardButton(text='🍲 Поесть', callback_data='category-reminder-admin_Поесть')
    btn_8 = types.InlineKeyboardButton(text='🚶 Прогулка', callback_data='category-reminder-admin_Прогулка')
    btn_9 = types.InlineKeyboardButton(text='😴 Отдохнуть', callback_data='category-reminder-admin_Отдохнуть')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_get-week', style='danger')
    markup.inline_keyboard.append([btn_1, btn_2])
    markup.inline_keyboard.append([btn_3, btn_4])
    markup.inline_keyboard.append([btn_5, btn_6])
    markup.inline_keyboard.append([btn_7, btn_8])
    markup.inline_keyboard.append([btn_9])
    markup.inline_keyboard.append([btn_back])
    return markup


async def select_time_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Интервальное напоминание', callback_data='select-time-type-reminder-admin_interval')
    btn_2 = types.InlineKeyboardButton(text='Раз в день', callback_data='select-time-type-reminder-admin_one')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_get-comment', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_back])
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
        days_dict[day] += " ✅"

    btn_1 = types.InlineKeyboardButton(text=days_dict['Понедельник'], callback_data='add-day-to-remind-admin_Понедельник')
    btn_2 = types.InlineKeyboardButton(text=days_dict['Вторник'], callback_data='add-day-to-remind-admin_Вторник')
    btn_3 = types.InlineKeyboardButton(text=days_dict['Среда'], callback_data='add-day-to-remind-admin_Среда')
    btn_4 = types.InlineKeyboardButton(text=days_dict['Четверг'], callback_data='add-day-to-remind-admin_Четверг')
    btn_5 = types.InlineKeyboardButton(text=days_dict['Пятница'], callback_data='add-day-to-remind-admin_Пятница')
    btn_6 = types.InlineKeyboardButton(text=days_dict['Суббота'], callback_data='add-day-to-remind-admin_Суббота')
    btn_7 = types.InlineKeyboardButton(text=days_dict['Воскресенье'], callback_data='add-day-to-remind-admin_Воскресенье')
    btn_8 = types.InlineKeyboardButton(text="Каждый день", callback_data='add-day-to-remind-admin_all-days')
    btn_9 = types.InlineKeyboardButton(text="Далее", callback_data='go-to-select-time-remind-admin')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_time-type', style='danger')
    markup.inline_keyboard.append([btn_1, btn_2])
    markup.inline_keyboard.append([btn_3, btn_4])
    markup.inline_keyboard.append([btn_5, btn_6])
    markup.inline_keyboard.append([btn_7, btn_8])
    markup.inline_keyboard.append([btn_9])
    markup.inline_keyboard.append([btn_back])
    return markup


async def time_settings_interval(current_hour: str, current_minute: str, selected_mode: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_up_hour = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-admin-remind-interval_up_hour')
    btn_up_minute = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-admin-remind-interval_up_minute')
    btn_hour = types.InlineKeyboardButton(text=current_hour, callback_data='---')
    btn_minute = types.InlineKeyboardButton(text=current_minute, callback_data='---')
    btn_down_hour = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-admin-remind-interval_down_hour')
    btn_down_minute = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-admin-remind-interval_down_minute')

    markup.inline_keyboard.append([btn_up_hour, btn_up_minute])
    markup.inline_keyboard.append([btn_hour, btn_minute])
    markup.inline_keyboard.append([btn_down_hour, btn_down_minute])

    if selected_mode == 'any-reminds-zero':
        btn_add = types.InlineKeyboardButton(text='Добавить', callback_data='add-time-interval-remind-admin')
        markup.inline_keyboard.append([btn_add])

    else:
        btn_add = types.InlineKeyboardButton(text='Добавить', callback_data='add-time-interval-remind-admin')
        btn_ready = types.InlineKeyboardButton(text='Готово', callback_data='go-to-save-remind-admin')
        markup.inline_keyboard.append([btn_add])
        markup.inline_keyboard.append([btn_ready])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_select-days', style='danger')
    markup.inline_keyboard.append([btn_back])

    return markup


async def time_settings_one(current_hour: str, current_minute: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_up_hour = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-admin-remind-one_up_hour')
    btn_up_minute = types.InlineKeyboardButton(text='⬆️', callback_data='time-settings-admin-remind-one_up_minute')
    btn_hour = types.InlineKeyboardButton(text=current_hour, callback_data='---')
    btn_minute = types.InlineKeyboardButton(text=current_minute, callback_data='---')
    btn_down_hour = types.InlineKeyboardButton(text='⬇️', callback_data='time-settings-admin-remind-one_down_hour')
    btn_down_minute = types.InlineKeyboardButton(text='⬇️',callback_data='time-settings-admin-remind-one_down_minute')


    markup.inline_keyboard.append([btn_up_hour, btn_up_minute])
    markup.inline_keyboard.append([btn_hour, btn_minute])
    markup.inline_keyboard.append([btn_down_hour, btn_down_minute])

    btn_add = types.InlineKeyboardButton(text='Готово', callback_data='go-to-save-remind-admin')
    markup.inline_keyboard.append([btn_add])


    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_time-type', style='danger')
    markup.inline_keyboard.append([btn_back])

    return markup


async def yes_or_no(select_prefix: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data=f'{select_prefix}_yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data=f'{select_prefix}_no')
    markup.inline_keyboard.append([btn_yes, btn_no])
    return markup


async def add_remind_or_no():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='save-remind-admin_yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='save-remind-admin_no')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_time-settings', style='danger')
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
                btn = types.InlineKeyboardButton(text=f'{obj["category"]} {obj["comment"][:20]}',callback_data=f'select-remind-delete-admin_{obj["id"]}')
                markup.inline_keyboard.append([btn])
        else:
            for obj in data[item_cnt * page: (item_cnt * page) + item_cnt]:
                obj = obj.__dict__
                btn = types.InlineKeyboardButton(text=f'{obj["category"]} {obj["comment"][:20]}', callback_data=f'select-remind-delete-admin__{obj["id"]}')
                markup.inline_keyboard.append([btn])

            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-remind-admin_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'Стр. {page + 1}/{all_pages}', callback_data=f'---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-remind-admin_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-pregnant-admin_select-action', style='danger')
        markup.inline_keyboard.append([btn_back])

        return markup

    else:
        return None





























