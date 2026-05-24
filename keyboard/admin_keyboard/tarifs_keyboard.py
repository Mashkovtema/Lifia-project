from aiogram import types


async def select_tarifs_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Стандартный', callback_data='select-tarif-admin_standart')
    btn_2 = types.InlineKeyboardButton(text='Про тариф', callback_data='select-tarif-admin_pro')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    return markup


async def tarif_settings():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Название', callback_data='select-tarif-setting_name')
    btn_2 = types.InlineKeyboardButton(text='Цена', callback_data='select-tarif-setting_cost')
    btn_3 = types.InlineKeyboardButton(text='Кол-во сообщений', callback_data='select-tarif-setting_message-cnt')
    btn_4 = types.InlineKeyboardButton(text='Фото', callback_data='select-tarif-setting_photo')
    btn_5 = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-tarif-redact-admin', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    return markup


async def add_or_back():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Добавить', callback_data='add-new-tarif-admin')
    btn_2 = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-tarif-redact-admin', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn])
    return markup
























