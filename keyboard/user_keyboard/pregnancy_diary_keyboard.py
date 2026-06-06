from aiogram import types


async def diary_main_buttons(data: dict):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    if data:
        if data['mood'] == '---':
            btn_mood = types.InlineKeyboardButton(text='Как я себя чувствую', callback_data='how-im-feeling_yes')
        else:
            btn_mood = types.InlineKeyboardButton(text='Как я себя чувствую ✅', callback_data='how-im-feeling_no')

        if data['photo'] == '---':
            btn_add_photo = types.InlineKeyboardButton(text='Добавить фото недели', callback_data='add-week-photo_yes')
        else:
            btn_add_photo = types.InlineKeyboardButton(text='Добавить фото недели ✅', callback_data='add-week-photo_no')


    else:
        btn_mood = types.InlineKeyboardButton(text='Как я себя чувствую', callback_data='how-im-feeling_yes')
        btn_add_photo = types.InlineKeyboardButton(text='Добавить фото недели', callback_data='add-week-photo_yes')


    btn_create = types.InlineKeyboardButton(text='Создать альбом', callback_data='create-album')
    btn_album = types.InlineKeyboardButton(text='Мой альбом беременности', callback_data='get-my-album')

    markup.inline_keyboard.append([btn_mood])
    markup.inline_keyboard.append([btn_add_photo])
    markup.inline_keyboard.append([btn_create])
    markup.inline_keyboard.append([btn_album])

    return markup


async def mood_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='😁', callback_data='select-my-mood_Хорошо')
    btn_2 = types.InlineKeyboardButton(text='🙁', callback_data='select-my-mood_Средне')
    btn_3 = types.InlineKeyboardButton(text='😫', callback_data='select-my-mood_Плохо')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-diary-user_main', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_back])
    return markup


async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn_back])
    return markup


async def pagination_buttons(data: list, page: int):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    if len(data) != 1:
        if page == 0:
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-photos_{data.index(data[-1])}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-photos_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        elif page == data.index(data[-1]):
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-photos_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-photos_')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        else:
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-photos_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-photos_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-diary-user_main', style='danger')
    markup.inline_keyboard.append([btn_back])

    return markup















