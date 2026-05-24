from aiogram import types


async def select_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Для беременных', callback_data='select-type-admin-chelenge_Для беременных')
    btn_2 = types.InlineKeyboardButton(text='Для родивших', callback_data='select-type-admin-chelenge_Для родивших')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    return markup


async def select_action():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_delete = types.InlineKeyboardButton(text='Удалить', callback_data='action-chelenge-admin_delete')
    btn_add = types.InlineKeyboardButton(text='Добавить', callback_data='action-chelenge-admin_add')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-main-chelenge-admin', style='danger')
    markup.inline_keyboard.append([btn_delete])
    markup.inline_keyboard.append([btn_add])
    markup.inline_keyboard.append([btn_back])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn_back])
    return markup


async def add_or_back():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='add-new-challenge-or-no_yes', style='success')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='add-new-challenge-or-no_no', style='danger')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-buttons-admin-challenges_bonus-cnt')
    markup.inline_keyboard.append([btn_yes, btn_no])
    markup.inline_keyboard.append([btn_back])
    return markup


async def delete_or_back():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='delete-challenge-or-no_yes', style='success')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='delete-challenge-or-no_no', style='danger')
    markup.inline_keyboard.append([btn_yes, btn_no])
    return markup


async def select_challenge(data: list):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    for challenge in data:
        challenge = challenge.__dict__
        btn = types.InlineKeyboardButton(text=challenge['name'], callback_data=f'select-challenge-to-delete_{challenge["id"]}')
        markup.inline_keyboard.append([btn])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-buttons-admin-challenges_week-delete', style='success')
    markup.inline_keyboard.append([btn_back])
    return markup















