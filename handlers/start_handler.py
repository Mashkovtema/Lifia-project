from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import Command, StateFilter
    
import logging
import datetime
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import start_keyboard
from database.requests import admin_requests, user_requests
from utils import utils

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
            text = await utils.get_text_by_type(user_in_db['mom_or_not'])
            markup = await start_keyboard.main_user_buttons(user_in_db['mom_or_not'])
            await message.answer(text=text, reply_markup=markup)
        else:
            text = ('Привет! Я ILIFIA 💜\n'
                    'Твой заботливый помощник во время беременности.\n'
                    'Я здесь 24/7 — чтобы поддерживать тебя на каждом шаге этого пути 🌸\n\n'
                    '😌 Отвечаю на любые вопросы о беременности\n'
                    '💙 Поддерживаю, когда тревожно или страшно\n'
                    '👶 Рассказываю, что сейчас происходит с малышом\n'
                    '✅ Помогаю подготовиться к родам спокойно\n'
                    '📋 Дневник и важные моменты беременности')

            markup = await start_keyboard.start_button()
            await message.answer(text=text, reply_markup=markup)


@router.callback_query(F.data == 'go-to-get-name-start')
async def go_to_get_name(callback: types.CallbackQuery, state: FSMContext):
    """Запрос имени"""
    logging.info('get_name')
    await callback.message.edit_text('Давай познакомимся 💜\n\nКак тебя зовут?')
    await state.set_state(FsmStart.get_name)


@router.message(StateFilter(FsmStart.get_name))
async def get_name(message: types.Message, state: FSMContext):
    """Получение имени пользователя"""
    logging.info('get_name')
    name = str(message.text)
    markup = await start_keyboard.select_type()
    text = (f'Красивое имя 💜\n'
            f'{name}, подскажи на каком ты этапе ?')
    await message.answer(text=text, reply_markup=markup)
    await state.update_data(name=name)
    await state.set_state(default_state)


@router.callback_query(F.data == 'select-start-not-mom')
async def im_not_mom(callback: types.CallbackQuery, state: FSMContext):
    """Переход в раздел я скоро стану мамой"""
    logging.info('im_not_mom')
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month

    state_data = await state.get_data()
    markup = await start_keyboard.days_buttons(current_month, current_year)

    text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
            f'Чтобы я могла следить за твоей беременностью — выбери дату первого дня последней менструации:')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(mom_or_not=False)


@router.callback_query(F.data == 'select-start-mom')
async def im_mom(callback: types.CallbackQuery, state: FSMContext):
    """Переход в раздел я ужэ мама"""
    logging.info('im_mom')
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month

    state_data = await state.get_data()
    markup = await start_keyboard.days_buttons(current_month, current_year)

    text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
            f'Чтобы я могла следить за развитием малыша — выбери дату рождения')

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
                f'Чтобы я могла следить за развитием малыша — выбери дату рождения')
    else:
        text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
                f'Чтобы я могла следить за твоей беременностью — выбери дату первого дня последней менструации:')

    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('select-mom-start-date_'))
async def select_date(callback: types.CallbackQuery, state: FSMContext):
    """Выбор даты"""
    logging.info('')
    year = int(str(callback.data).split('_')[1])
    month = int(str(callback.data).split('_')[2])
    day = int(str(callback.data).split('_')[3])
    await state.update_data()

    state_data = await state.get_data()
    day_cnt, week = await utils.calculate_days(year, month, day)

    if day_cnt == -1:
        await callback.answer('Выбрана дата в будущем, измените выбор ❌')
    elif day_cnt > 280:
        await callback.message.edit_text('Выбрана некорректная дата, попробуйте еще раз ❌')
    else:
        markup = await start_keyboard.troubles_buttons(state_data['mom_or_not'])
        if state_data['mom_or_not']:
            text = await user_requests.get_text_by_days_cnt(day_cnt, 'mom')
        else:
            text = await user_requests.get_text_by_days_cnt(day_cnt, 'not-mom')

        await callback.message.edit_text(text=text, reply_markup=markup)
        await state.update_data(week=week)
        await state.update_data(day_cnt=day_cnt)


@router.callback_query(F.data.startswith('select-mom-trouble-start_'))
async def select_trouble(callback: types.CallbackQuery, state: FSMContext):
    """Выбор того что волнует"""
    logging.info('select_trouble')
    trouble = str(callback.data).split('_')[1]
    if trouble == 'Другое':
        markup = await start_keyboard.back_button('back-start-user_select-trouble')
        await callback.message.edit_text('Напиши, что тебя беспокоит 💙\n\n'
                                         'Здесь можно написать всё — страх, боль, тревогу, странное ощущение. Я отвечу сразу и помогу разобраться.', reply_markup=markup)
        await state.set_state(FsmStart.get_trouble)
    else:
        state_data = await state.get_data()
        tarif_data = await user_requests.get_tarifs_data('standart')
        markup = await start_keyboard.select_pro_or_default_tarif('standart')
        text = await utils.get_text_by_type(state_data['mom_or_not'])

        await callback.message.delete()
        await callback.message.answer_photo(photo=tarif_data['photo'], caption=text, reply_markup=markup)
        await state.update_data(trouble=trouble)
        await state.update_data(subscription_type='standart')


@router.message(StateFilter(FsmStart.get_trouble))
async def get_trouble(message: types.Message, state: FSMContext):
    """Получение проблемы """
    logging.info('get_trouble')
    trouble = str(message.text)
    state_data = await state.get_data()
    tarif_data = await user_requests.get_tarifs_data('standart')
    markup = await start_keyboard.select_pro_or_default_tarif('standart')
    text = await utils.get_text_by_type(state_data['mom_or_not'])

    await message.answer_photo(photo=tarif_data['photo'], caption=text, reply_markup=markup)
    await state.update_data(trouble=trouble)


@router.callback_query(F.data.startswith('watch-tarif-user-start_'))
async def watch_another_tarif(callback: types.CallbackQuery, state: FSMContext):
    """Просмотр другого тарифа"""
    logging.info('watch_another_tarif')
    tarif_type = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    tarif_data = await user_requests.get_tarifs_data(tarif_type)
    markup = await start_keyboard.select_pro_or_default_tarif(tarif_type)

    text = await utils.get_text_by_type(state_data['mom_or_not'])

    await callback.message.delete()
    await callback.message.answer_photo(photo=tarif_data['photo'], caption=text, reply_markup=markup)
    await state.update_data(subscription_type=tarif_type)


@router.callback_query(F.data == 'go-to-get-time-zone-start')
async def go_to_select_tarif_type(callback: types.CallbackQuery, state: FSMContext):
    """Переход к выбору часового пояса"""
    logging.info('go_to_select_tarif_type')
    markup = await start_keyboard.time_zone_buttons()
    await callback.message.delete()
    await callback.message.answer('💜 Выбери свой часовой пояс для напоминаний', reply_markup=markup)
    await state.set_state(default_state)


@router.callback_query(F.data.startswith('MSK+'))
async def select_time_zone(callback: types.CallbackQuery, state: FSMContext):
    """Выбор часового пояса"""
    logging.info('select_time_zone')
    time_zone = int(str(callback.data).split("+")[1])
    user_id = int(callback.from_user.id)
    username = str(callback.from_user.username)

    await state.update_data(time_zone=time_zone)

    state_data = await state.get_data()
    text = await utils.get_text_by_type(state_data['mom_or_not'])
    markup = await start_keyboard.main_user_buttons(state_data['mom_or_not'])

    await user_requests.add_new_user(state_data, user_id, username)
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=markup)
    await state.clear()
    await state.set_state(default_state)



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

    if flag == 'date':
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month

        state_data = await state.get_data()
        markup = await start_keyboard.days_buttons(current_month, current_year)

        if state_data['mom_or_not']:
            text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
                    f'Теперь выбери дату рождения малыша')
        else:
            text = (f'Спасибо, {state_data["name"]}! 💜\n\n'
                    f'Теперь выбери дату первого дня последней менструации:')

        await callback.message.edit_text(text=text, reply_markup=markup)

    if flag == 'select-trouble':
        markup = await start_keyboard.troubles_buttons(state_data['mom_or_not'])
        if state_data['mom_or_not']:
            text = f'Текст для мам, малышу {state_data["week"]} недель'
        else:
            text = (f'💜 Сейчас у тебя\n'
                    f'{state_data["week"]} неделя беременности\n\n'
                    f'👶 Малыш уже начинает слышать звуки вокруг и реагировать на них.\n\n'
                    f'🤍 На этом сроке многие женщины чувствуют усталость и эмоциональные перепады — это нормально.\n\n'
                    f'Что тебя волнует больше всего?')
        await callback.message.edit_text(text=text, reply_markup=markup)



























