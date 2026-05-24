from aiogram import types


async def change_token_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Сменить ключ', callback_data='change-token-admin')
    markup.inline_keyboard.append([btn])
    return markup


async def back_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data='back-to-ai-token-admin', style='danger')
    markup.inline_keyboard.append([btn])
    return markup