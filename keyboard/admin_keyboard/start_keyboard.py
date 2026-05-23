from aiogram import types


async def main_buttons():
    markup = types.ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    btn_1 = types.KeyboardButton(text='Напоминания ⏰')
    btn_2 = types.KeyboardButton(text='Ключ к ии моделям 🗝')
    btn_3 = types.KeyboardButton(text='Создать рассылку 🗝')
    btn_4 = types.KeyboardButton(text='Редактировать тарифы ⚙️')
    btn_5 = types.KeyboardButton(text='Выгрузка пользователей 👥')
    btn_6 = types.KeyboardButton(text='Обучение модели 🤖')
    btn_7 = types.KeyboardButton(text='Списки задач 📋')
    markup.keyboard.append([btn_1, btn_2])
    markup.keyboard.append([btn_3, btn_4])
    markup.keyboard.append([btn_5, btn_6])
    markup.keyboard.append([btn_7])
    return markup