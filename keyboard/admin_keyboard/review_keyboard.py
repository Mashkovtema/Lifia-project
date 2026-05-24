from aiogram import types


async def reviews_pagination(data: list, page: int):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    btn_commit = types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm-moderation-review_{page}')
    btn_delete = types.InlineKeyboardButton(text='Удалить', callback_data=f'delete-review_{page}')
    markup.inline_keyboard.append([btn_commit, btn_delete])

    if page == 0:
        btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-admin-reviews-moderation_{data.index(data[-1])}')
        btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
        btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-admin-reviews-moderation_{page + 1}')
        markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

    elif page == data.index(data[-1]):
        btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-admin-reviews-moderation_{page - 1}')
        btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
        btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-admin-reviews-moderation_0')
        markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

    else:
        btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-admin-reviews-moderation_{page - 1}')
        btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
        btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-admin-reviews-moderation_{page + 1}')
        markup.inline_keyboard.append([btn_back, btn_page, btn_forward])
    return markup


async def yes_or_no_buttons(yes_callback: str, no_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data=yes_callback, style='success')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data=no_callback, style='danger')
    markup.inline_keyboard.append([btn_yes, btn_no])
    return markup