from aiogram import Router, types, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import chelenges_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


class FsmAdminChallenges(StatesGroup):
    get_challenge_name = State()
    get_bonus_cnt = State()
    get_week = State()

    get_week_delete = State()


@router.message(F.text == 'Списки задач 📋')
async def chelenges_handler(message: types.Message, state: FSMContext):
    """Списки задач"""
    logging.info('chelenges_handler')
    markup = await chelenges_keyboard.select_type()
    await message.answer('Выберите категорию задач 👇', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == 'back-to-main-chelenge-admin')
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    """Назад к главной"""
    logging.info('back-to-main')
    markup = await chelenges_keyboard.select_type()
    await callback.message.edit_text('Выберите категорию задач 👇', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data.startswith('select-type-admin-chelenge_'))
async def select_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор типа задач"""
    logging.info('select_type')
    category = str(callback.data).split('_')[1]
    markup = await chelenges_keyboard.select_action()
    await callback.message.edit_text('Выберите действие 👇', reply_markup=markup)
    await state.update_data(category=category)


#######################################################################
########################№№ Удаление задачи ############################
#######################################################################


@router.callback_query(F.data == 'action-chelenge-admin_delete')
async def delete_chellenges(callback: types.CallbackQuery, state: FSMContext):
    """Удаление задач"""
    logging.info('delete_chellenges')
    markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_action')
    await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
    await state.set_state(FsmAdminChallenges.get_week_delete)


@router.message(StateFilter(FsmAdminChallenges.get_week_delete))
async def get_week_to_delete(message: types.Message, state: FSMContext):
    """Получение недели для удаленя"""
    logging.info('get_week_to_delete')
    week = str(message.text)
    check_week = await utils.validate_int_data(week)
    state_data = await state.get_data()
    if check_week:
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], int(week))
        if challenges_data:
            markup = await chelenges_keyboard.select_challenge(challenges_data)
            await message.answer(text='Выберите напоминание 👇', reply_markup=markup)
            await state.update_data(week=int(week))
        else:
            markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_week-delete')
            await message.answer('На этой неделе нет ни одной задачи ❌', reply_markup=markup)
    else:
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_week-delete')
        await message.answer('На этой неделе нет ни одной задачи ❌', reply_markup=markup)


@router.callback_query(F.data.startswith('select-challenge-to-delete_'))
async def select_challenge_to_delete(callback: types.CallbackQuery, state: FSMContext):
    """Выбор задачи для удаления"""
    logging.info('select_challenge_to_delete')
    index = int(str(callback.data).split('_')[1])
    challenge_data = await admin_requests.get_challenge_by_index(index)
    markup = await chelenges_keyboard.delete_or_back()

    text = (f'Вы уверены что хотите удалить задачу ?\n\n'
            f'📆 Неделя - {challenge_data["week"]}\n'
            f'📄 Задача - {challenge_data["name"]}\n'
            f'💎 Кол-во бонусов - {challenge_data["bonus_cnt"]}')

    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.update_data(index=index)


@router.callback_query(F.data.startswith('delete-challenge-or-no_'))
async def delete_challenge_or_no(callback: types.CallbackQuery, state: FSMContext):
    """Удалять задачу или нет"""
    logging.info('delete_challenge_or_no')
    flag = str(callback.data).split('_')[1]
    state_data = await state.get_data()
    if flag == 'yes':
        await admin_requests.delete_challenge(state_data['index'])

        week = state_data['week']
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], int(week))
        if challenges_data:
            markup = await chelenges_keyboard.select_challenge(challenges_data)
            await callback.message.edit_text(text='Выберите напоминание 👇', reply_markup=markup)
        else:
            markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_week-delete')
            await callback.message.edit_text('На этой неделе нет ни одной задачи ❌', reply_markup=markup)
        await callback.answer('Напоминание удалено ✅')

    else:
        week = state_data['week']
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], int(week))
        markup = await chelenges_keyboard.select_challenge(challenges_data)
        await callback.message.edit_text(text='Выберите напоминание 👇', reply_markup=markup)


#######################################################################
######################## Добавление задачи ############################
#######################################################################


@router.callback_query(F.data == 'action-chelenge-admin_add')
async def add_new_chelenge(callback: types.CallbackQuery, state: FSMContext):
    """Добавлентие новой задачи"""
    logging.info('add_new_chelenge')
    markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_action')
    await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
    await state.set_state(FsmAdminChallenges.get_week)


@router.message(StateFilter(FsmAdminChallenges.get_week))
async def get_week(message: types.Message, state: FSMContext):
    """Получение недели"""
    logging.info('get_week')
    week = str(message.text)
    check_week = await utils.validate_int_data(week)
    state_data = await state.get_data()
    if check_week:
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], int(week))
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_week')
        if challenges_data:
            text = (f'📆 Неделя - {week}\n'
                    f'Имеющиеся задачи: \n\n')

            for challenge in challenges_data:
                challenge = challenge.__dict__
                text += f'* {challenge["name"]} - {challenge["bonus_cnt"]} 💎\n'

            text += '\nВведите новую задачу 👇'
        else:
            text = (f'📆 Неделя - {week}\n'
                    f'Имеющихся задач нет\n\n'
                    f'Введите новую задачу 👇')

        await message.answer(text=text, reply_markup=markup)
        await state.set_state(FsmAdminChallenges.get_challenge_name)
        await state.update_data(week=int(week))

    else:
        await message.answer('Введена некорректная неделя, попробуйте еща раз ❌')


@router.message(StateFilter(FsmAdminChallenges.get_challenge_name))
async def get_challenge_name(message: types.Message, state: FSMContext):
    """Получение названия задачи"""
    logging.info('get_challenge_name')
    name = str(message.text)
    state_data = await state.get_data()
    challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], state_data['week'])
    markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_name')
    if challenges_data:
        text = (f'📆 Неделя - {state_data["week"]}\n'
                f'Имеющиеся задачи: \n\n')

        for challenge in challenges_data:
            challenge = challenge.__dict__
            text += f'* {challenge["name"]} - {challenge["bonus_cnt"]} 💎\n'

        text += '\nВведите кол-во бонусов начисляемых за задачу 👇'
    else:
        text = (f'📆 Неделя - {state_data["week"]}\n'
                f'Имеющихся задач нет\n\n'
                f'Введите кол-во бонусов начисляемых за задачу 👇')

    await message.answer(text=text, reply_markup=markup)
    await state.set_state(FsmAdminChallenges.get_bonus_cnt)
    await state.update_data(name=name)


@router.message(StateFilter(FsmAdminChallenges.get_bonus_cnt))
async def get_bonus_cnt(message: types.Message, state: FSMContext):
    """Получение кол-ва бонусов"""
    logging.info('get_bonus_cnt')
    bonus_cnt = str(message.text)
    check_week = await utils.validate_int_data(bonus_cnt)
    state_data = await state.get_data()
    if check_week:
        text = (f'Вы уверены что хотите добавить задачу ?\n\n'
                f'📆 Неделя - {state_data["week"]}\n'
                f'📄 Задача - {state_data["name"]}\n'
                f'💎 Кол-во бонусов - {bonus_cnt}')

        markup = await chelenges_keyboard.add_or_back()
        await message.answer(text=text, reply_markup=markup)
        await state.update_data(bonus_cnt=bonus_cnt)
    else:
        await message.answer('Введена некорректная сумма, попробуйте еща раз ❌')


@router.callback_query(F.data.startswith('add-new-challenge-or-no_'))
async def add_new_challenge_or_no(callback: types.CallbackQuery, state: FSMContext):
    """Добавлять новую задачу или нет"""
    logging.info('add_new_challenge_or_no')
    flag = str(callback.data).split('_')[1]
    if flag == 'yes':
        state_data = await state.get_data()
        await admin_requests.add_new_challenge(state_data)
        await callback.message.edit_text('Задача успешно добавлена ✅')
        await state.clear()
        await state.set_state(default_state)
    else:
        await callback.message.edit_text('Добавление задачи отменено ❌')
        await state.clear()
        await state.set_state(default_state)


@router.callback_query(F.data.startswith('back-buttons-admin-challenges_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]
    await state.set_state(default_state)
    state_data = await state.get_data()
    if flag == 'action':
        markup = await chelenges_keyboard.select_action()
        await callback.message.edit_text('Выберите действие 👇', reply_markup=markup)\

    if flag == 'week':
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_action')
        await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
        await state.set_state(FsmAdminChallenges.get_week)

    if flag == 'week-delete':
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_action')
        await callback.message.edit_text('Введите неделю 👇', reply_markup=markup)
        await state.set_state(FsmAdminChallenges.get_week_delete)

    if flag == 'name':
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], state_data["week"])
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_week')
        if challenges_data:
            text = (f'📆 Неделя - {state_data["week"]}\n'
                    f'Имеющиеся задачи: \n\n')

            for challenge in challenges_data:
                challenge = challenge.__dict__
                text += f'* {challenge["name"]} - {challenge["bonus_cnt"]} 💎\n'

            text += '\nВведите новую задачу 👇'
        else:
            text = (f'📆 Неделя - {state_data["week"]}\n'
                    f'Имеющихся задач нет\n\n'
                    f'Введите новую задачу 👇')

        await callback.message.edit_text(text=text, reply_markup=markup)
        await state.set_state(FsmAdminChallenges.get_challenge_name)

    if flag == 'bonus-cnt':
        challenges_data = await admin_requests.get_chelenges_by_category(state_data['category'], state_data['week'])
        markup = await chelenges_keyboard.back_button('back-buttons-admin-challenges_name')
        if challenges_data:
            text = (f'📆 Неделя - {state_data["week"]}\n'
                    f'Имеющиеся задачи: \n\n')

            for challenge in challenges_data:
                challenge = challenge.__dict__
                text += f'* {challenge["name"]} - {challenge["bonus_cnt"]} 💎\n'

            text += '\nВведите кол-во бонусов начисляемых за задачу 👇'
        else:
            text = (f'📆 Неделя - {state_data["week"]}\n'
                    f'Имеющихся задач нет\n\n'
                    f'Введите кол-во бонусов начисляемых за задачу 👇')

        await callback.message.edit_text(text=text, reply_markup=markup)
        await state.set_state(FsmAdminChallenges.get_bonus_cnt)



















