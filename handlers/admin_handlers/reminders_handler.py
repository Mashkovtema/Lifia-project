from aiogram import Router, types, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import reminders_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


class FsmRemindersAdmin(StatesGroup):
    get_week = State()
    get_comment = State()


@router.message(F.text == 'Напоминания ⏰')
async def reminders_main(message: types.Message, state: FSMContext):
    """Раздел напоминаний"""
    logging.info('reminders_main')
    markup = await reminders_keyboard.select_type()
    await message.answer('Выберите категорию пользователей для уведомлений 👇', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data.startswith('select-remind-type-admin_'))
async def select_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор типа пользователей"""
    logging.info('select_type')
    users_type = str(callback.data).split('_')[1]
    markup = await reminders_keyboard.add_delete_or_back()
    await callback.message.edit_text('Выберите действие 👇', reply_markup=markup)
    await state.update_data(users_type=users_type)


###################################################################
##################### Удаление напоминаний ######################
###################################################################


@router.callback_query(F.data == 'select-action-reminders-admin_delete')
async def delete_reminds(callback: types.CallbackQuery, state: FSMContext):
    """Начало удаления напомианний"""
    logging.info('delete_reminds')
    state_data = await state.get_data()
    reminds = await admin_requests.get_reminds_by_type(state_data['users_type'])
    if reminds:
        markup = await reminders_keyboard.delete_reminds(reminds, 0)
        await callback.message.edit_text('Активные напоминания 👇', reply_markup=markup)
        await state.update_data(page=0)
    else:
        await callback.answer('Вы еще не добавили ни одного напоминания ❌')


@router.callback_query(F.data.startswith('pagination-remind-admin_'))
async def pagination(callback: types.CallbackQuery, state: FSMContext):
    """Пагинация"""
    logging.info('pagination')
    page = int(str(callback.data).split('_')[1])
    state_data = await state.get_data()
    reminds = await admin_requests.get_reminds_by_type(state_data['users_type'])
    markup = await reminders_keyboard.delete_reminds(reminds, page)

    if markup:
        await callback.message.edit_text('Активные напоминания 👇', reply_markup=markup)
        await callback.answer()
        await state.update_data(page=page)
    else:
        await callback.answer()


@router.callback_query(F.data.startswith('select-remind-delete-admin_'))
async def select_remind_to_delete(callback: types.CallbackQuery, state: FSMContext):
    """Выбор напоминания"""
    logging.info('select_remind_to_delete')
    index = int(str(callback.data).split('_')[1])
    remind = await admin_requests.get_remind_by_index(index)
    markup = await reminders_keyboard.yes_or_no('delete-remind-admin')

    category = remind['category']
    time_type = remind['time_type']
    selected_times = remind['times']
    comment = remind['comment']
    selected_days = remind['days']
    users_type = remind['users_type']

    text = (f'Вы уверены что хотите удалить напоминание ?\n\n'
            f'📄 Тип: {category}\n\n'
            f'⏰ Частота: {time_type}\n\n'
            f'🕘 Время: {selected_times}\n\n'
            f'📆 Дни: {selected_days}\n\n'
            f'👥 Категория пользователей: {users_type}\n\n'
            f'✉️ Комментарий: {comment}')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(index=index)


@router.callback_query(F.data.startswith('delete-remind-admin_'))
async def confirm_or_not_delete_remind(callback: types.CallbackQuery, state: FSMContext):
    """Удалять напомианание или нет"""
    logging.info('confirm_or_not_delete_remind')
    flag = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    if flag == 'yes':
        markup = await reminders_keyboard.back_button('select-action-reminders-admin_delete')
        await admin_requests.delete_remind_by_index(state_data['index'])
        await callback.message.edit_text('Напоминание успешно удалено ✅', reply_markup=markup)
    else:
        reminds = await admin_requests.get_reminds_by_type(state_data['users_type'])
        markup = await reminders_keyboard.delete_reminds(reminds, state_data['page'])

        await callback.message.edit_text('Активные напоминания 👇', reply_markup=markup)
        await callback.answer()


###################################################################
##################### Добавление напоминаний ######################
###################################################################


@router.callback_query(F.data == 'select-action-reminders-admin_add')
async def add_new_remind(callback: types.CallbackQuery, state: FSMContext):
    """Добавление нового напоминания, запрос недели"""
    logging.info('add_new_remind')
    markup = await reminders_keyboard.back_button('back-pregnant-admin_select-action')
    await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
    await state.set_state(FsmRemindersAdmin.get_week)


@router.message(StateFilter(FsmRemindersAdmin.get_week))
async def get_week(message: types.Message, state: FSMContext):
    """Получение недели"""
    logging.info('get_week')
    try:
        week = int(message.text)
        if week >= 0:
            markup = await reminders_keyboard.select_category()
            await message.answer('Выберите категорию напоминания 👇', reply_markup=markup)
            await state.set_state(default_state)
            await state.update_data(week=week)
        else:
            markup = await reminders_keyboard.back_button('back-pregnant-admin_select-action')
            await message.answer('Введено некорректное число, попробуйте еще раз ❌', reply_markup=markup)
    except Exception as e:
        logging.info(f'Error: {e}')
        markup = await reminders_keyboard.back_button('back-pregnant-admin_select-action')
        await message.answer('Введено некорректное число, попробуйте еще раз ❌', reply_markup=markup)


@router.callback_query(F.data.startswith('category-reminder-admin_'))
async def get_category(callback: types.CallbackQuery, state: FSMContext):
    """Получение категории напоминания"""
    logging.info('get_category')
    category_old = str(callback.data).split('_')[1]
    category = await utils.add_sticker_to_category(category_old)
    markup = await reminders_keyboard.back_button('back-pregnant-admin_select-category')
    await callback.message.edit_text('Введите комментарий для напоминания 👇', reply_markup=markup)
    await state.set_state(FsmRemindersAdmin.get_comment)
    await state.update_data(category=category)


@router.message(StateFilter(FsmRemindersAdmin.get_comment))
async def get_comment(message: types.Message, state: FSMContext):
    """Получение комментария"""
    logging.info('get_comment')
    comment = str(message.text)
    markup = await reminders_keyboard.select_time_type()
    await message.answer('Выберите периодичность напоминания 👇', reply_markup=markup)
    await state.set_state(default_state)
    await state.update_data(comment=comment)


@router.callback_query(F.data.startswith('select-time-type-reminder-admin_'))
async def select_time_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор периодичности напоминания"""
    logging.info('select_time_type')
    time_type = str(callback.data).split('_')[1]
    if time_type == 'interval':
        markup = await reminders_keyboard.select_days_to_remind([])
        await callback.message.edit_text('Выберите дни недели для напоминания 👇', reply_markup=markup)
        await state.update_data(days=[])
        await state.update_data(time_type='Интервальное напоминание')
    else:
        markup = await reminders_keyboard.time_settings_one('Часы', 'Минуты')
        selected_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        await callback.message.edit_text('Настройте время для напоминания 👇', reply_markup=markup)
        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=[])
        await state.update_data(time_type='Раз в день')
        await state.update_data(days=selected_days)


@router.callback_query(F.data.startswith('time-settings-admin-remind-one_'))
async def time_settings_for_interval(callback: types.CallbackQuery, state: FSMContext):
    """Выбор времени для напоминания"""
    logging.info('time_settings_for_interval')
    state_data = await state.get_data()
    action = str(callback.data).split('_')[1]
    flag = str(callback.data).split('_')[2]

    current_hour = state_data['current_hour']
    current_minute = state_data['current_minute']

    text = 'Настройте время для напоминания 👇'

    new_current_hour, new_current_minute = await utils.process_time_settings(int(current_hour), int(current_minute), action, flag)
    selected_times = [f'{new_current_hour}:{new_current_minute}']
    markup = await reminders_keyboard.time_settings_one(new_current_hour, new_current_minute)
    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except:
        await callback.answer()

    await state.update_data(current_hour=new_current_hour)
    await state.update_data(current_minute=new_current_minute)
    await state.update_data(selected_times=selected_times)


@router.callback_query(F.data.startswith('add-day-to-remind-admin_'))
async def add_days_to_remind(callback: types.CallbackQuery, state: FSMContext):
    """Выбор дня для напоминания"""
    logging.info('add_days_to_remind')
    day = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    selected_days = state_data['days']

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


@router.callback_query(F.data == 'go-to-select-time-remind-admin')
async def go_to_time_settings_interval(callback: types.CallbackQuery, state: FSMContext):
    """Начало настройки времен для многодневного напоминания"""
    logging.info('go_to_time_settings_interval')
    state_data = await state.get_data()
    if len(state_data['days']) > 0:
        markup = await reminders_keyboard.time_settings_interval('Часы', 'Минуты', 'any-reminds-zero')
        await callback.message.edit_text('Настройте время для напоминания 👇', reply_markup=markup)
        await state.set_state(default_state)
        await state.update_data(current_hour='12')
        await state.update_data(current_minute='00')
        await state.update_data(selected_times=[])
        await state.update_data(status='any-reminds-zero')
    else:
        await callback.answer('Выберите хотябы 1 день')

@router.callback_query(F.data.startswith('time-settings-admin-remind-interval_'))
async def time_settings_for_interval(callback: types.CallbackQuery, state: FSMContext):
    """Выбор времени для напоминания"""
    logging.info('time_settings_for_interval')
    state_data = await state.get_data()
    action = str(callback.data).split('_')[1]
    flag = str(callback.data).split('_')[2]

    current_hour = int(state_data['current_hour'])
    current_minute = int(state_data['current_minute'])
    selected_times = state_data['selected_times']
    status = state_data['status']

    if len(selected_times) == 0:
        text = 'Настройте время для напоминания 👇'
    else:
        text = f'Выбранные времена 👇\n'
        for time in selected_times:
            text += f'* {time}\n'

        text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'

    new_current_hour, new_current_minute = await utils.process_time_settings(int(current_hour), int(current_minute), action, flag)
    markup = await reminders_keyboard.time_settings_interval(new_current_hour, new_current_minute, status)
    try:
        await callback.message.edit_text(text=text, reply_markup=markup)
    except:
        await callback.answer()

    await state.update_data(current_hour=new_current_hour)
    await state.update_data(current_minute=new_current_minute)


@router.callback_query(F.data == 'add-time-interval-remind-admin')
async def add_time_to_interval_remind(callback: types.CallbackQuery, state: FSMContext):
    """Добавленире времени к интервальному напоминанию"""
    logging.info('add_time_to_interval_remind')
    state_data = await state.get_data()

    current_hour = state_data['current_hour']
    current_minute = state_data['current_minute']
    selected_times = state_data['selected_times']

    if f'{current_hour}:{current_minute}' not in selected_times:
        selected_times.append(f'{current_hour}:{current_minute}')

        text = f'Выбранные времена 👇\n'
        for time in selected_times:
            text += f'* {time}\n'

        text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'
        markup = await reminders_keyboard.time_settings_interval('Часы', 'Минуты', 'any-reminds-added')
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


@router.callback_query(F.data == 'go-to-save-remind-admin')
async def go_to_save_remind(callback: types.CallbackQuery, state: FSMContext):
    """Выводим информацию по напоминанию"""
    logging.info('go_to_save_remind')
    state_data = await state.get_data()

    category = state_data['category']
    time_type = state_data['time_type']
    selected_times = ', '.join(state_data['selected_times'])
    comment = state_data['comment']
    selected_days = ', '.join(state_data['days'])
    users_type = state_data['users_type']

    text = (f'Вы уверены что хотите добавить напоминание ?\n\n'
            f'📄 Тип: {category}\n\n'
            f'⏰ Частота: {time_type}\n\n'
            f'🕘 Время: {selected_times}\n\n'
            f'📆 Дни: {selected_days}\n\n'
            f'👥 Категория пользователей: {users_type}\n\n'
            f'✉️ Комментарий: {comment}')

    markup = await reminders_keyboard.add_remind_or_no()
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('save-remind-admin_'))
async def save_remind_or_no(callback: types.CallbackQuery, state: FSMContext):
    """Добавлять напоминание или нет"""
    logging.info('save_remind_or_no')
    flag = str(callback.data).split('_')[1]
    if flag == 'no':
        await callback.message.edit_text('Добавление напоминания отменено ❌')
        await state.clear()
        await state.set_state(default_state)

    else:
        state_data = await state.get_data()
        category = state_data['category']
        time_type = state_data['time_type']
        selected_times = ', '.join(state_data['selected_times'])
        selected_days = ', '.join(state_data['days'])
        comment = state_data['comment']
        users_type = state_data['users_type']

        await admin_requests.add_new_admin_remind(category, time_type, selected_times, selected_days, comment, users_type)
        await callback.message.edit_text('Напоминание успешно добавлено ✅')
        await state.set_state(default_state)
        await state.clear()


@router.callback_query(F.data.startswith('back-pregnant-admin_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]

    if flag == 'select-type':
        markup = await reminders_keyboard.select_type()
        await callback.message.edit_text('Выберите категорию пользователей для уведомлений 👇', reply_markup=markup)
        await state.clear()

    if flag == 'select-action':
        markup = await reminders_keyboard.add_delete_or_back()
        await callback.message.edit_text('Выберите действие 👇', reply_markup=markup)

    if flag == 'get-week':
        markup = await reminders_keyboard.back_button('back-pregnant-admin_select-action')
        await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
        await state.set_state(FsmRemindersAdmin.get_week)

    if flag == 'select-category':
        markup = await reminders_keyboard.select_category()
        await callback.message.edit_text('Выберите категорию напоминания 👇', reply_markup=markup)

    if flag == 'get-comment':
        markup = await reminders_keyboard.back_button('back-pregnant-admin_select-category')
        await callback.message.edit_text('Введите комментарий для напоминания 👇', reply_markup=markup)
        await state.set_state(FsmRemindersAdmin.get_comment)

    if flag == 'time-type':
        markup = await reminders_keyboard.select_time_type()
        await callback.message.edit_text('Выберите периодичность напоминания 👇', reply_markup=markup)
        await state.set_state(default_state)

    if flag == 'select-days':
        state_data = await state.get_data()

        if len(state_data['selected_times']) == 0:
            selected_days = state_data['days']
            markup = await reminders_keyboard.select_days_to_remind(selected_days)
            await callback.message.edit_text('Выберите дни недели для напоминания 👇', reply_markup=markup)
            await state.update_data(days=selected_days)
            await state.update_data(status='any-reminds-zero')
        else:
            selected_times = state_data['selected_times']
            selected_times.pop()

            current_hour = '12'
            current_minute = '00'

            if len(selected_times) == 0:
                status = 'any-reminds-zero'
            else:
                status = 'any-reminds-added'

            if len(selected_times) == 0:
                text = 'Настройте время для напоминания 👇'
            else:
                text = f'Выбранные времена 👇\n'
                for time in selected_times:
                    text += f'* {time}\n'

                text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'

            markup = await reminders_keyboard.time_settings_interval(current_hour, current_minute, status)
            try:
                await callback.message.edit_text(text=text, reply_markup=markup)
            except:
                await callback.answer()

            await state.update_data(current_hour=current_hour)
            await state.update_data(current_minute=current_minute)
            await state.update_data(selected_times=selected_times)
            await state.update_data(status=status)

    if flag == 'time-settings':
        state_data = await state.get_data()
        if state_data['time_type'] == 'Интервальное напоминание':
            current_hour = state_data['current_hour']
            current_minute = state_data['current_minute']
            selected_times = state_data['selected_times']
            status = state_data['status']

            text = f'Выбранные времена 👇\n'
            for time in selected_times:
                text += f'* {time}\n'

            text += '\nВыберите время и нажмите кнопку "Добавить" чтобы добавить еще, либо на кнопку "Готово" чтобы продолжить'
            markup = await reminders_keyboard.time_settings_interval(current_hour, current_minute, status)
            try:
                await callback.message.edit_text(text=text, reply_markup=markup)
            except:
                await callback.answer()

        else:
            current_hour = state_data['current_hour']
            current_minute = state_data['current_minute']

            text = 'Настройте время для напоминания 👇'
            markup = await reminders_keyboard.time_settings_one(current_hour, current_minute)
            try:
                await callback.message.edit_text(text=text, reply_markup=markup)
            except:
                await callback.answer()













