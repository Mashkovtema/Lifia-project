from aiogram import types


async def select_category():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Отзывы мам', callback_data='select-category-reviews-user_reviews')
    btn_2 = types.InlineKeyboardButton(text='Оставить отзыв', callback_data='select-category-reviews-user_send-review')
    btn_3 = types.InlineKeyboardButton(text='Предложения', callback_data='select-category-reviews-user_suggestion')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    return markup



async def back_button(back_callback: str):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data=back_callback, style='danger')
    markup.inline_keyboard.append([btn])
    return markup


async def pagination_reviews_buttons(data: list, page: int):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    if len(data) != 1:

        if page == 0:
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-reviews_{data.index(data[-1])}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-reviews_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        elif page == data.index(data[-1]):
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-reviews_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-reviews_0')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

        else:
            btn_back = types.InlineKeyboardButton(text='<<<', callback_data=f'pagination-user-reviews_{page - 1}')
            btn_page = types.InlineKeyboardButton(text=f'{page + 1}/{len(data)}', callback_data='---')
            btn_forward = types.InlineKeyboardButton(text='>>>', callback_data=f'pagination-user-reviews_{page + 1}')
            markup.inline_keyboard.append([btn_back, btn_page, btn_forward])

    btn_back_main = types.InlineKeyboardButton(text='Назад', callback_data='back-user-reviews_main', style='danger')
    markup.inline_keyboard.append([btn_back_main])

    return markup


async def select_grade_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='⭐️', callback_data='select-grade-user_1')
    btn_2 = types.InlineKeyboardButton(text='⭐️⭐️', callback_data='select-grade-user_2')
    btn_3 = types.InlineKeyboardButton(text='⭐️⭐️⭐️', callback_data='select-grade-user_3')
    btn_4 = types.InlineKeyboardButton(text='⭐️⭐️⭐️⭐️', callback_data='select-grade-user_4')
    btn_5 = types.InlineKeyboardButton(text='⭐️⭐️⭐️⭐️⭐️', callback_data='select-grade-user_5')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-user-reviews_main', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    markup.inline_keyboard.append([btn_back])
    return markup


async def yes_or_no_or_back_review():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='send-review-or-not_yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='send-review-or-not_no')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-user-reviews_get-comment', style='danger')
    markup.inline_keyboard.append([btn_yes, btn_no])
    markup.inline_keyboard.append([btn_back])
    return markup


async def yes_or_no_or_back_suggestion():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='send-suggestion-or-not_yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='send-suggestion-or-not_no')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-user-reviews_get-suggestion', style='danger')
    markup.inline_keyboard.append([btn_yes, btn_no])
    markup.inline_keyboard.append([btn_back])
    return markup















