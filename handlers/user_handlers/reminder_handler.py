import logging
from datetime import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter

from config_data.config_data import Config, load_config
from keyboard.user_keyboard import reminders_keyboard
from database.requests import user_requests
from utils import utils

config: Config = load_config()
router = Router()


class FsmRemindersUser(StatesGroup):
    get_name = State()
    get_week = State()
    get_comment = State()


@router.message(F.text == 'Напоминания 🔔')
async def reminders_user(message: types.Message, state: FSMContext):
    """Раздел с напоминаниями пользователя"""
    logging.info('reminders_user')
    markup = await reminders_keyboard.main_remind_buttons()
    await message.answer(text='💜 О чем тебе напоминать? Я помогу тебе не забывать о важном для тебя',
                         reply_markup=markup)
    await state.clear()


########################################
####### Добавление напоминания #########
########################################


@router.callback_query(F.data.startswith('select-remind-category-user_'))
async def select_remind_category(callback: types.CallbackQuery, state: FSMContext):
    """Выбор категории напоминания"""
    logging.info('select_remind_category')
    category = str(callback.data).split('_')[1]
    if category == 'health':
        markup = await reminders_keyboard.health_category_buttons()
    elif category == 'important':
        markup = await reminders_keyboard.important_category_buttons()
    else:
        markup = await reminders_keyboard.back_button('back-reminds-user_main')
        await state.set_state(FsmRemindersUser.get_name)

    await state.update_data(main_category=category)
    await callback.message.edit_text('💜 О чем тебе напоминать?', reply_markup=markup)


@router.callback_query(F.data.startswith('type-reminder-user_'))
async def select_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор типа напоминания"""
    logging.info('select_type')
    reminder_type = str(callback.data).split('_')[1]
    markup = await reminders_keyboard.select_remind_type()
    await callback.message.edit_text('💜 Как тебе удобнее получать напоминания?', reply_markup=markup)
    await state.update_data(category=reminder_type)


@router.message(StateFilter(FsmRemindersUser.get_name))
async def get_name(message: types.Message, state: FSMContext):
    """Получение типа напоминания (для своего напоминания)"""
    logging.info('get_name')
    category = str(message.text)
    markup = await reminders_keyboard.select_remind_type()
    await message.answer('💜 Как тебе удобнее получать напоминания?', reply_markup=markup)
    await state.update_data(category=category)


@router.callback_query(F.data.startswith('select-time-type-reminder-user_'))
async def select_time_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор периодичности напоминания"""
    logging.info('select_time_type')
    time_type = str(callback.data).split('_')[1]

    if time_type == 'interval':
        markup = await reminders_keyboard.select_days_to_remind([])
        await callback.message.edit_text('Выберите дни недели для напоминания 👇', reply_markup=markup)
        await state.update_data(days=[])
        await state.update_data(time_type='Интервальное напоминание')

    elif time_type == 'date':
        current_month = int(datetime.now().month)
        current_year = int(datetime.now().year)
        markup = await reminders_keyboard.days_period_buttons(current_month, current_year)
        await callback.message.edit_text('💜 Выбери дату когда хочешь получить напоминание?', reply_markup=markup)
        await state.update_data(time_type='Определенная дата')
        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=['12:00'])

    else:  # one - раз в день
        markup = await reminders_keyboard.time_settings_one('12', '00')
        selected_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        await callback.message.edit_text('Настройте время для напоминания 👇', reply_markup=markup)
        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=['12:00'])
        await state.update_data(time_type='Раз в день')
        await state.update_data(days=selected_days)


@router.callback_query(F.data.startswith('pagination-date-remind-user_'))
async def pagination_date(callback: types.CallbackQuery, state: FSMContext):
    """Пагинация даты"""
    logging.info('pagination_date')
    current_month = int(str(callback.data).split('_')[1])
    current_year = int(str(callback.data).split('_')[2])
    markup = await reminders_keyboard.days_period_buttons(current_month, current_year)
    await callback.message.edit_text('💜 Выбери дату когда хочешь получить напоминание?', reply_markup=markup)
    await state.update_data(time_type='Определенная дата')


@router.callback_query(F.data.startswith('select-date-to-remind-user_'))
async def select_date_to_remind(callback: types.CallbackQuery, state: FSMContext):
    """Выбор даты для напоминания"""
    logging.info('select_date_to_remind')
    year = str(callback.data).split('_')[1]
    month = str(callback.data).split('_')[2]
    day = str(callback.data).split('_')[3]
    markup = await reminders_keyboard.time_settings_date('12', '00')
    await callback.message.edit_text('💜 Во сколько ты хочешь получить напоминание?', reply_markup=markup)
    await state.update_data(date=f'{day}.{month}.{year}')


@router.callback_query(F.data.startswith('time-settings-user-remind-date'))
async def edit_time_date_settings(callback: types.CallbackQuery, state: FSMContext):
    """Настройка времени для напоминания в определенную дату"""
    logging.info('edit_time_date_settings')
    state_data = await state.get_data()
    action = str(callback.data).split('_')[1]
    flag = str(callback.data).split('_')[2]

    current_hour = state_data['current_hour']
    current_minute = state_data['current_minute']

    text = '💜 Во сколько ты хочешь получить напоминание ?'

    new_current_hour, new_current_minute = await utils.process_time_settings(int(current_hour), int(current_minute),
                                                                             action, flag)
    markup = await reminders_keyboard.time_settings_date(new_current_hour, new_current_minute)
    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except:
        await callback.answer()

    await state.update_data(current_hour=new_current_hour)
    await state.update_data(current_minute=new_current_minute)


@router.callback_query(F.data.startswith('time-settings-user-remind-one_'))
async def time_settings_for_one(callback: types.CallbackQuery, state: FSMContext):
    """Выбор времени для ежедневного напоминания"""
    logging.info('time_settings_for_one')
    state_data = await state.get_data()
    action = str(callback.data).split('_')[1]
    flag = str(callback.data).split('_')[2]

    current_hour = state_data['current_hour']
    current_minute = state_data['current_minute']

    text = '💜 Во сколько ты хочешь получить напоминание ?'

    new_current_hour, new_current_minute = await utils.process_time_settings(int(current_hour), int(current_minute),
                                                                             action, flag)
    selected_times = [f'{new_current_hour}:{new_current_minute}']
    markup = await reminders_keyboard.time_settings_one(new_current_hour, new_current_minute)
    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except:
        await callback.answer()

    await state.update_data(current_hour=new_current_hour)
    await state.update_data(current_minute=new_current_minute)
    await state.update_data(selected_times=selected_times)


@router.callback_query(F.data.startswith('add-day-to-remind-user_'))
async def add_days_to_remind(callback: types.CallbackQuery, state: FSMContext):
    """Выбор дня для напоминания"""
    logging.info('add_days_to_remind')
    day = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    selected_days = state_data.get('days', [])

    if day == 'all-days':
        if len(selected_days) == 7:
            selected_days = []
        else:
            selected_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    else:
        if day not in selected_days:
            selected_days.append(day)
        else:
            selected_days.remove(day)

    markup = await reminders_keyboard.select_days_to_remind(selected_days)
    await callback.message.edit_text('Выберите дни недели для напоминания 👇', reply_markup=markup)
    await state.update_data(days=selected_days)


@router.callback_query(F.data == 'go-to-select-time-remind-user')
async def go_to_time_settings_interval(callback: types.CallbackQuery, state: FSMContext):
    """Начало настройки времен для интервального напоминания"""
    logging.info('go_to_time_settings_interval')
    state_data = await state.get_data()
    if len(state_data.get('days', [])) > 0:
        markup = await reminders_keyboard.time_settings_interval('12', '00', 'any-reminds-zero')
        await callback.message.edit_text('Настройте время для напоминания 👇', reply_markup=markup)
        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=[])
        await state.update_data(status='any-reminds-zero')
    else:
        await callback.answer('Выберите хотя бы 1 день')


@router.callback_query(F.data.startswith('time-settings-user-remind-interval_'))
async def time_settings_for_interval(callback: types.CallbackQuery, state: FSMContext):
    """Выбор времени для интервального напоминания"""
    logging.info('time_settings_for_interval')
    state_data = await state.get_data()
    action = str(callback.data).split('_')[1]
    flag = str(callback.data).split('_')[2]

    current_hour = int(state_data.get('current_hour', 12))
    current_minute = int(state_data.get('current_minute', 0))
    selected_times = state_data.get('selected_times', [])
    status = state_data.get('status', 'any-reminds-zero')

    if len(selected_times) == 0:
        text = 'Настройте время для напоминания 👇'
    else:
        text = f'Выбранные времена 👇\n'
        for time in selected_times:
            text += f'* {time}\n'
        text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'

    new_current_hour, new_current_minute = await utils.process_time_settings(current_hour, current_minute, action, flag)
    markup = await reminders_keyboard.time_settings_interval(new_current_hour, new_current_minute, status)
    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except:
        await callback.answer()

    await state.update_data(current_hour=new_current_hour)
    await state.update_data(current_minute=new_current_minute)


@router.callback_query(F.data == 'add-time-interval-remind-user')
async def add_time_to_interval_remind(callback: types.CallbackQuery, state: FSMContext):
    """Добавление времени к интервальному напоминанию"""
    logging.info('add_time_to_interval_remind')
    state_data = await state.get_data()

    current_hour = state_data.get('current_hour', '12')
    current_minute = state_data.get('current_minute', '00')
    selected_times = state_data.get('selected_times', [])

    time_str = f'{current_hour}:{current_minute}'

    if time_str not in selected_times:
        selected_times.append(time_str)
        selected_times.sort()  # Сортируем времена

        text = f'Выбранные времена 👇\n'
        for time in selected_times:
            text += f'* {time}\n'
        text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'
        markup = await reminders_keyboard.time_settings_interval('12', '00', 'any-reminds-added')
        try:
            await callback.message.edit_text(text=text, reply_markup=markup)
        except:
            await callback.answer()

        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=selected_times)
        await state.update_data(status='any-reminds-added')
    else:
        await callback.answer('Это время уже добавлено')


@router.callback_query(F.data == 'go-to-save-remind-user-date')
async def go_to_save_remind_user(callback: types.CallbackQuery, state: FSMContext):
    """Переход к запросу заметки"""
    logging.info('go_to_save_remind_user')
    await callback.message.edit_text('💜 Введи заметку для напоминания')
    await state.set_state(FsmRemindersUser.get_comment)


@router.message(StateFilter(FsmRemindersUser.get_comment))
async def get_comment(message: types.Message, state: FSMContext):
    """Получение комментария и показ подтверждения"""
    logging.info('get_comment')
    comment = str(message.text)
    await state.update_data(comment=comment)
    state_data = await state.get_data()
    markup = await reminders_keyboard.add_or_no_or_back_buttons()

    category = state_data.get('category', 'Не указано')
    time_type = state_data.get('time_type', 'Не указано')
    comment = state_data.get('comment', 'Не указано')

    if time_type == 'Определенная дата':
        date = state_data.get('date', 'Не указана')
        current_hour = state_data.get('current_hour', '12')
        current_minute = state_data.get('current_minute', '00')

        text = (f'Вы уверены что хотите добавить напоминание?\n\n'
                f'📄 Тип: {category}\n\n'
                f'⏰ Частота: {time_type}\n\n'
                f'🕘 Время: {current_hour}:{current_minute}\n\n'
                f'📆 Дата: {date}\n\n'
                f'✉️ Комментарий: {comment}')

    elif time_type == 'Раз в день':
        selected_times = ', '.join(state_data.get('selected_times', ['Не указано']))
        selected_days = 'Каждый день'

        text = (f'Вы уверены что хотите добавить напоминание?\n\n'
                f'📄 Тип: {category}\n\n'
                f'⏰ Частота: {time_type}\n\n'
                f'🕘 Время: {selected_times}\n\n'
                f'📆 Дни: {selected_days}\n\n'
                f'✉️ Комментарий: {comment}')

    else:  # Интервальное напоминание
        selected_times = ', '.join(state_data.get('selected_times', ['Не указано']))
        selected_days = ', '.join(state_data.get('days', ['Не указано']))

        text = (f'Вы уверены что хотите добавить напоминание?\n\n'
                f'📄 Тип: {category}\n\n'
                f'⏰ Частота: {time_type}\n\n'
                f'🕘 Время: {selected_times}\n\n'
                f'📆 Дни: {selected_days}\n\n'
                f'✉️ Комментарий: {comment}')

    await message.answer(text=text, reply_markup=markup)


@router.callback_query(F.data == 'add-new-remind-user-question_yes')
async def save_reminder(callback: types.CallbackQuery, state: FSMContext):
    """Сохранение напоминания в базу данных"""
    logging.info('save_reminder')
    state_data = await state.get_data()
    user_id = callback.from_user.id

    # Получаем все данные для сохранения
    reminder_data = {
        'user_id': user_id,
        'category': state_data.get('category'),
        'comment': state_data.get('comment'),
        'time_type': state_data.get('time_type'),
        'days': ', '.join(state_data.get('days', ['Не указано'])),
        'selected_times': ', '.join(state_data.get('selected_times')),
        'date': state_data.get('date'),
    }
    logging.info(f'reminder_data: {reminder_data}')

    await user_requests.add_new_remind(reminder_data)
    await callback.message.edit_text('✅ Напоминание успешно добавлено!')
    await state.clear()


@router.callback_query(F.data == 'add-new-remind-user-question_no')
async def cancel_save_reminder(callback: types.CallbackQuery, state: FSMContext):
    """Отмена сохранения напоминания"""
    logging.info('cancel_save_reminder')
    await callback.message.edit_text('❌ Добавление напоминания отменено')
    await state.clear()


#########################################
########### Мои напоминания #############
#########################################


@router.callback_query(F.data == 'my-reminds-user')
async def my_reminds_user(callback: types.CallbackQuery, state: FSMContext):
    """Напоминания пользователя"""
    logging.info('my_reminds_user')
    markup = await reminders_keyboard.select_remind_type_my_reminds()
    await callback.message.edit_text('💜 Выбери категорию напоминаний', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data.startswith('select-my-remind-user_'))
async def select_remind_user(callback: types.CallbackQuery, state: FSMContext):
    """выбор типа напоминаний"""
    logging.info('select_remind_user')
    category = str(callback.data).split("_")[1]
    user_id = int(callback.from_user.id)
    reminds_data = await user_requests.get_my_reminds_by_category(user_id, category)
    if reminds_data:
        markup = await reminders_keyboard.delete_reminds(reminds_data, 0)
        await callback.message.edit_text('💜Выбери напоминание для удаления', reply_markup=markup)
        await state.update_data(category=category)
        await state.set_state(default_state)
        await state.update_data(page=0)
    else:
        await callback.answer('💜У тебя нет напоминаний в этой категории')


@router.callback_query(F.data.startswith('pagination-remind-user_'))
async def pagination(callback: types.CallbackQuery, state: FSMContext):
    """Пагинация напоминаний"""
    logging.info('pagination')
    page = int(str(callback.data).split('_')[1])
    user_id = int(callback.from_user.id)
    state_data = await state.get_data()
    reminds_data = await user_requests.get_my_reminds_by_category(user_id, state_data['category'])
    markup = await reminders_keyboard.delete_reminds(reminds_data, page)
    if markup:
        await callback.message.edit_text('💜Выбери напоминание для удаления', reply_markup=markup)
        await state.update_data(page=page)
    else:
        await callback.answer()


@router.callback_query(F.data.startswith('select-remind-delete-user_'))
async def select_remind_delete_user(callback: types.CallbackQuery, state: FSMContext):
    """Выбор напоминания для удаления"""
    logging.info('select_remind_delete_user')
    index = int(str(callback.data).split('_')[1])
    state_data = await state.get_data()
    markup = await reminders_keyboard.delete_or_no_reminds(state_data['page'])
    remind_data = await user_requests.get_remind_by_index_and_category(state_data['category'], index)

    if state_data['category'] == 'date':
        text = (f'Вы уверены что хотите удалить напоминание?\n\n'
                f'📄 Тип: {remind_data["category"]}\n\n'
                f'🕘 Время: {remind_data["time"]}\n\n'
                f'📆 Дата: {remind_data["date"]}\n\n'
                f'✉️ Комментарий: {remind_data["comment"]}')

    elif state_data['category'] == 'one':
        text = (f'Вы уверены что хотите удалить напоминание?\n\n'
                f'📄 Тип: {remind_data["category"]}\n\n'
                f'🕘 Время: {remind_data["time"]}\n\n'
                f'📆 Дни: каждый день\n\n'
                f'✉️ Комментарий: {remind_data["comment"]}')

    else:  # Интервальное напоминание
        text = (f'Вы уверены что хотите удалить напоминание?\n\n'
                f'📄 Тип: {remind_data["category"]}\n\n'
                f'🕘 Время: {remind_data["times"]}\n\n'
                f'📆 Дни: {remind_data["days"]}\n\n'
                f'✉️ Комментарий: {remind_data["comment"]}')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(index=index)


@router.callback_query(F.data.startswith('confirm-delete-remind'))
async def confirm_delete_remind(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение удаления напоминания"""
    logging.info('confirm_delete_remind')
    state_data = await state.get_data()
    category = state_data['category']
    index = state_data['index']

    await user_requests.delete_remind(category, index)

    reminds_data = await user_requests.get_my_reminds_by_category(category)
    if reminds_data:
        markup = await reminders_keyboard.delete_reminds(reminds_data, 0)
        await callback.message.edit_text('💜Выбери напоминание для удаления', reply_markup=markup)
        await state.update_data(category=category)
        await state.set_state(default_state)
    else:
        await callback.message.edit_text('💜У тебя нет напоминаний в этой категории')


##############################
### Обработка кнопок назад ###
##############################


@router.callback_query(F.data.startswith('back-reminds-user_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]

    if flag == 'main':
        markup = await reminders_keyboard.main_remind_buttons()
        await callback.message.edit_text(text='💜 О чем тебе напоминать? Я помогу тебе не забывать о важном для тебя',
                                         reply_markup=markup)
        await state.clear()

    elif flag == 'category':
        state_data = await state.get_data()
        main_category = state_data.get('main_category', 'health')

        if main_category == 'health':
            markup = await reminders_keyboard.health_category_buttons()
        elif main_category == 'important':
            markup = await reminders_keyboard.important_category_buttons()
        else:
            markup = await reminders_keyboard.back_button('back-reminds-user_main')

        await callback.message.edit_text('💜 О чем тебе напоминать?', reply_markup=markup)

    elif flag == 'select-type':
        markup = await reminders_keyboard.select_remind_type()
        await callback.message.edit_text('💜 Как тебе удобнее получать напоминания?', reply_markup=markup)

    elif flag == 'get-comment':
        await callback.message.edit_text('💜 Введи заметку для напоминания')
        await state.set_state(FsmRemindersUser.get_comment)

    elif flag == 'interval-remind':
        state_data = await state.get_data()

        selected_times = state_data.get('selected_times', [])

        if selected_times:
            selected_times.pop()
            selected_times.sort()  # Сортируем времена

            text = f'Выбранные времена 👇\n'
            for time in selected_times:
                text += f'* {time}\n'
            text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'
            markup = await reminders_keyboard.time_settings_interval('12', '00', 'any-reminds-added')
            try:
                await callback.message.edit_text(text=text, reply_markup=markup)
            except:
                await callback.answer()

            await state.update_data(selected_times=selected_times)
            await state.update_data(status='any-reminds-added')

        else:
            selected_days = state_data.get('days', [])
            markup = await reminders_keyboard.select_days_to_remind(selected_days)
            await callback.message.edit_text('Выберите дни недели для напоминания 👇', reply_markup=markup)
            await state.update_data(days=selected_days)
            await state.update_data(status='not-any-reminds-added')

    elif flag == 'catedory-delete':
        markup = await reminders_keyboard.select_remind_type_my_reminds()
        await callback.message.edit_text('💜 Выбери категорию напоминаний', reply_markup=markup)
        await state.clear()
        await state.set_state(default_state)





##############################
####### Дополнительные обработчики для теста
##############################


@router.callback_query(F.data == 'ignore')
async def ignore_callback(callback: types.CallbackQuery):
    """Игнорирование нажатий на пустые кнопки"""
    await callback.answer()


















