from aiogram import types


async def challenges_buttons(data: list, user_data: int):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    for challenge in data:
        index = data.index(challenge) + 1
        challenge = challenge.__dict__
        if challenge['id'] in user_data:
            btn = types.InlineKeyboardButton(text=f'{index} ✅', callback_data=f'uncomplete-challenge-user_{challenge["id"]}')
        else:
            btn = types.InlineKeyboardButton(text=f'{index}', callback_data=f'complete-challenge-user_{challenge["id"]}')
        markup.inline_keyboard.append([btn])

    btn_points = types.InlineKeyboardButton(text='Трекер очков', callback_data='how-many-points')
    markup.inline_keyboard.append([btn_points])

    return markup


async def back_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data='back-to-my-tasks', style='danger')
    markup.inline_keyboard.append([btn])
    return markup