from aiogram import types


async def select_users_type():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_not_mom = types.InlineKeyboardButton(text='Беременные', callback_data='select-user-to-mail-admin_not-mom')
    btn_mom = types.InlineKeyboardButton(text='Родившие', callback_data='select-user-to-mail-admin_mom')
    btn_all = types.InlineKeyboardButton(text='Все', callback_data='select-user-to-mail-admin_all')
    markup.inline_keyboard.append([btn_not_mom])
    markup.inline_keyboard.append([btn_mom])
    markup.inline_keyboard.append([btn_all])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn_back])
    return markup


async def send_or_back_or_delete(type: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_send = types.InlineKeyboardButton(text='Отправить', callback_data='send-mail-now')
    btn_cancel = types.InlineKeyboardButton(text='Отменить', callback_data='cancel-mail-admin')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data=f'select-user-to-mail-admin_{type}', style='danger')
    markup.inline_keyboard.append([btn_send, btn_cancel])
    markup.inline_keyboard.append([btn_back])
    return markup