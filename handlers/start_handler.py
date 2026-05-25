from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import Command, StateFilter
    
import logging
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import start_keyboard

from database.requests import admin_requests, user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')

def extract_arg(arg):
    return arg.split()[1:]


class FsmStart(StatesGroup):
    get_name = State()
    get_trouble = State()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    """Старт"""
    logging.info(f'start: {message.from_user.id}')
    user_id = int(message.from_user.id)

    if str(user_id) in admin_ids:
        markup = await start_keyboard.main_buttons()
        await message.answer('Вы администратор, выберите действие:', reply_markup=markup)
    else:
        user_in_db = await user_requests.check_user(user_id)
        if user_in_db:
            pass
        else:
            text = ('Привет! Я ILIFIA 💜\n\n'
                    'Твой заботливый помощник во время беременности\n\n'
                    'Я рядом 24/7, чтобы поддерживатьтебя на каждом этапе 😊\n\n'
                    '😌 Отвечаю на любые вопросы о беременности\n\n'
                    '💙 Поддерживаю в тревожные моменты\n\n'
                    '👶 Рассказываю, что происходит с малышом\n\n'
                    '✅ Помогаю подготовиться к родам\n\n'
                    '📋 Дневник и важные заметки беременности')

            markup = await start_keyboard.start_button()
            await message.answer(text=text, reply_markup=markup)


@router.callback_query(F.data == 'go-to-get-name-start')
async def go_to_get_name(callback: types.CallbackQuery, state: FSMContext):
    """Запрос имени"""
    logging.info('get_name')
    await callback.message.edit_text('Давай познакомимся поближе 💜\n\nКак тебя зовут?')
    await state.set_state(FsmStart.get_name)


@router.message(StateFilter(FsmStart.get_name))
async def get_name(message: types.Message, state: FSMContext):
    """Получение имени пользователя"""
    logging.info('get_name')
    name = str(message.text)
    markup = await start_keyboard.select_type()
    text = f'💙 {name}, подскажи на каком ты этапе ?'
    await message.answer(text=text, reply_markup=markup)
    await state.update_data(name=name)
    await state.set_state(default_state)


#################################################
############ Скоро станет мамой #################
#################################################


@router.callback_query(F.data == 'select-start-not-mom')
async def im_not_mom(callback: types.CallbackQuery, state: FSMContext):
    """Переход в раздел я скоро стану мамой"""
    logging.info('im_not_mom')
    state_data = await state.get_data()
    markup = await start_keyboard.days_buttons(5, 2026)

    text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
            f'Теперь выбери дату первого дня последней менструации:')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(mom_or_not=False)


@router.callback_query(F.data == 'select-start-mom')
async def im_mom(callback: types.CallbackQuery, state: FSMContext):
    """Переход в раздел я ужэ мама"""
    logging.info('im_mom')
    state_data = await state.get_data()
    markup = await start_keyboard.days_buttons(5, 2026)

    text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
            f'Теперь выбери дату рождения малыша')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(mom_or_not=True)


@router.callback_query(F.data.startswith('mom-start-date_'))
async def pagination_date(callback: types.CallbackQuery, state: FSMContext):
    """Пагинцаия даты"""
    logging.info('pagination_date')
    month = int(str(callback.data).split('_')[1])
    year = int(str(callback.data).split('_')[2])

    state_data = await state.get_data()
    markup = await start_keyboard.days_buttons(month, year)

    if state_data['mom_or_not']:
        text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
                f'Теперь выбери дату рождения малыша')
    else:
        text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
                f'Теперь выбери дату первого дня последней менструации:')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(mom_or_not=True)


@router.callback_query(F.data.startswith('select-mom-start-date_'))
async def select_date(callback: types.CallbackQuery, state: FSMContext):
    """Выбор даты"""
    logging.info('')
    year = int(str(callback.data).split('_')[1])
    month = int(str(callback.data).split('_')[2])
    day = int(str(callback.data).split('_')[3])

    state_data = await state.get_data()


















@router.callback_query(F.data.startswith('back-start-user_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    if flag == 'name':
        await callback.message.edit_text('Давай познакомимся поближе 💜\n\nКак тебя зовут?')
        await state.set_state(FsmStart.get_name)

    if flag == 'type':
        markup = await start_keyboard.select_type()
        text = f'💙 {state_data["name"]}, подскажи на каком ты этапе ?'
        await callback.message.edit_text(text=text, reply_markup=markup)



























