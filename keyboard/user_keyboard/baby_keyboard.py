from aiogram import types


async def razdels_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='🍼 Кормление', callback_data='select-baby-razdel_Кормление')
    btn_2 = types.InlineKeyboardButton(text='😴 Сон малыша', callback_data='select-baby-razdel_Сон малыша')
    btn_3 = types.InlineKeyboardButton(text='🛁 Гигиена и купание', callback_data='select-baby-razdel_Гигиена и купание')
    btn_4 = types.InlineKeyboardButton(text='🤒 Здоровье без паники', callback_data='select-baby-razdel_Здоровье без паники')
    btn_5 = types.InlineKeyboardButton(text='😢 Плач: что делать', callback_data='select-baby-razdel_Плач')
    btn_6 = types.InlineKeyboardButton(text='❤️ Мама, ты не одна', callback_data='select-baby-razdel_Ты не одна')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    markup.inline_keyboard.append([btn_6])
    return markup


async def feeding_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Грудь и смесь', callback_data='get-baby-user-text_1')
    btn_2 = types.InlineKeyboardButton(text='Как наладить лактацию', callback_data='get-baby-user-text_2')
    btn_3 = types.InlineKeyboardButton(text='Колики', callback_data='get-baby-user-text_3')
    btn_4 = types.InlineKeyboardButton(text='Срыгивания', callback_data='get-baby-user-text_4')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_back])
    return markup


async def sleep_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Сколько спит малыш', callback_data='get-baby-user-text_5')
    btn_2 = types.InlineKeyboardButton(text='Безопасные позы', callback_data='get-baby-user-text_6')
    btn_3 = types.InlineKeyboardButton(text='Как уложить — первые недели', callback_data='get-baby-user-text_7')
    btn_4 = types.InlineKeyboardButton(text='Ритуалы — с 6–8 недель', callback_data='get-baby-user-text_8')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_back])
    return markup


async def gigiena_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Первое купание', callback_data='get-baby-user-text_9')
    btn_2 = types.InlineKeyboardButton(text='Пупок', callback_data='get-baby-user-text_10')
    btn_3 = types.InlineKeyboardButton(text='Подгузник', callback_data='get-baby-user-text_11')
    btn_4 = types.InlineKeyboardButton(text='Стрижка ногтей', callback_data='get-baby-user-text_12')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_back])
    return markup


async def health_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Температура', callback_data='get-baby-user-text_13')
    btn_2 = types.InlineKeyboardButton(text='Насморк', callback_data='get-baby-user-text_14')
    btn_3 = types.InlineKeyboardButton(text='Кашель', callback_data='get-baby-user-text_15')
    btn_4 = types.InlineKeyboardButton(text='Стул', callback_data='get-baby-user-text_16')
    btn_5 = types.InlineKeyboardButton(text='Когда звонить немедленно', callback_data='get-baby-user-text_17')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_5])
    markup.inline_keyboard.append([btn_back])
    return markup


async def plach_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Как понять причину', callback_data='get-baby-user-text_18')
    btn_2 = types.InlineKeyboardButton(text='Как быстро успокоить', callback_data='get-baby-user-text_19')
    btn_3 = types.InlineKeyboardButton(text='Если ничего не помогает', callback_data='get-baby-user-text_20')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_back])
    return markup


async def mom_buttons():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn_1 = types.InlineKeyboardButton(text='Усталость', callback_data='get-baby-user-text_21')
    btn_2 = types.InlineKeyboardButton(text='Как попросить о помощи', callback_data='get-baby-user-text_22')
    btn_3 = types.InlineKeyboardButton(text='Послеродовая депрессия', callback_data='get-baby-user-text_23')
    btn_4 = types.InlineKeyboardButton(text='Если совсем тяжело', callback_data='get-baby-user-text_24')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn_1])
    markup.inline_keyboard.append([btn_2])
    markup.inline_keyboard.append([btn_3])
    markup.inline_keyboard.append([btn_4])
    markup.inline_keyboard.append([btn_back])
    return markup


async def back_or_ai_chat():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Давай поговорим', callback_data='chat-with-ai-user')
    btn_back = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-theme-baby', style='danger')
    markup.inline_keyboard.append([btn])
    markup.inline_keyboard.append([btn_back])
    return markup


async def back_button():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[])
    btn = types.InlineKeyboardButton(text='Назад', callback_data='back-to-select-razdel-baby', style='danger')
    markup.inline_keyboard.append([btn])
    return markup