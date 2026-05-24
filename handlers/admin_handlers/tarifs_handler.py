from aiogram import Router, types, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import tarifs_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


class FsmTarifAdmin(StatesGroup):
    get_new_data = State()
    get_name = State()
    get_cost = State()
    get_message_cnt = State()
    get_photo = State()


@router.message(F.text == 'Редактировать тарифы ⚙️')
async def redact_tarifs_handler(message: types.Message, state: FSMContext):
    """Редактирование тарифов"""
    logging.info('redact_tarifs_handler')
    markup = await tarifs_keyboard.select_tarifs_buttons()
    await message.answer('Выберите тариф для настройки 👇', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == 'back-to-select-tarif-redact-admin')
async def back_to_select_tarif(callback: types.CallbackQuery, state: FSMContext):
    """Назад к выбору типа тарифа"""
    logging.info('back_to_select_tarif')
    markup = await tarifs_keyboard.select_tarifs_buttons()
    await callback.message.delete()
    await callback.message.answer('Выберите тариф для настройки 👇', reply_markup=markup)
    await state.clear()


@router.callback_query(F.data.startswith('select-tarif-admin_'))
async def select_tarif(callback: types.CallbackQuery, state: FSMContext):
    """Выбор тарифа"""
    logging.info('select_tarif')
    tarif_type = str(callback.data).split('_')[1]
    tarif_data = await admin_requests.get_tarif_type(tarif_type)
    if tarif_data:
        markup = await tarifs_keyboard.tarif_settings()
        text = (f'📄 Название: {tarif_data["name"]}\n'
                f'💵 Цена: {tarif_data["cost"]}р\n'
                f'📩 Кол-во сообщений в день: {tarif_data["message_cnt"]}\n\n'
                f'Выберите параметр для изменения 👇')
        await callback.message.delete()
        await callback.message.answer_photo(photo=tarif_data['photo'], caption=text, reply_markup=markup)
        await state.update_data(tarif_data=tarif_data)
        await state.update_data(tarif_type=tarif_type)
    else:
        markup = await tarifs_keyboard.add_or_back()
        await callback.message.edit_text('Данный тип тарифа не установлен, '
                                         'нажмите на кнопку чтобы добавить данные по тарифу 👇',
                                         reply_markup=markup)
        await state.update_data(tarif_type=tarif_type)


@router.callback_query(F.data.startswith('select-tarif-setting_'))
async def select_new_data(callback: types.CallbackQuery, state: FSMContext):
    """Выбор параметра для редактирования"""
    logging.info('select_new_data')
    parametr = str(callback.data).split('_')[1]
    markup = await tarifs_keyboard.back_button('back-to-add-tarif_main-menu')
    state_data = await state.get_data()
    tarif_data = state_data['tarif_data']

    text = (f'📄 Название: {tarif_data["name"]}\n'
            f'💵 Цена: {tarif_data["cost"]}р\n'
            f'📩 Кол-во сообщений в день: {tarif_data["message_cnt"]}\n\n')

    if parametr == 'name':
        text += 'Введите новое название тарифа 👇'
    if parametr == 'cost':
        text += 'Введите новую цену тарифа 👇'
    if parametr == 'message-cnt':
        text += 'Введите новое кол-во сообщений к ИИ в день 👇'
    if parametr == 'photo':
        text += 'Отправьте новое фото для тарифа 👇'

    await state.set_state(FsmTarifAdmin.get_new_data)
    await state.update_data(parametr=parametr)
    await callback.message.edit_caption(caption=text, reply_markup=markup)


@router.message(StateFilter(FsmTarifAdmin.get_new_data))
async def get_new_data(message: types.Message, state: FSMContext):
    """Получение новых данных для тарифа"""
    logging.info('get_new_data')
    state_data = await state.get_data()
    parametr = state_data['parametr']
    new_data = str(message.text)
    check = False

    if parametr == 'name':
        await admin_requests.update_tarif_data(state_data['tarif_type'], parametr, new_data)
        check = True
    if parametr == 'cost':

        check_data = await utils.validate_int_data(new_data)
        if check_data:
            check = True
            await admin_requests.update_tarif_data(state_data['tarif_type'], parametr, new_data)
        else:
            await message.answer('Введена некорректная цена, попробуйте еще раз ❌')

    if parametr == 'message-cnt':

        check_data = await utils.validate_int_data(new_data)
        if check_data:
            check = True
            await admin_requests.update_tarif_data(state_data['tarif_type'], parametr, new_data)
        else:
            await message.answer('Введено некорректное кол-во сообщений, попробуйте еще раз ❌')

    if parametr == 'photo':

        if message.photo:
            file_id = message.photo[-1].file_id
            check = True
            await admin_requests.update_tarif_data(state_data['tarif_type'], parametr, file_id)
        else:
            await message.answer('Вы отправили не фото/видео, попробуйте еще раз ❌')

    if check:
        tarif_type = state_data['tarif_type']
        tarif_data = await admin_requests.get_tarif_type(tarif_type)
        markup = await tarifs_keyboard.tarif_settings()
        text = (f'📄 Название: {tarif_data["name"]}\n'
                f'💵 Цена: {tarif_data["cost"]}р\n'
                f'📩 Кол-во сообщений в день: {tarif_data["message_cnt"]}\n\n'
                f'Выберите параметр для изменения 👇')

        await message.answer_photo(photo=tarif_data['photo'], caption=text, reply_markup=markup)


@router.callback_query(F.data == 'add-new-tarif-admin')
async def start_add_new_tarif(callback: types.CallbackQuery, state: FSMContext):
    """Начало добавления данных по тарифу"""
    logging.info('start_add_new_tarif')
    markup = await tarifs_keyboard.back_button('back-to-select-tarif-redact-admin')
    await callback.message.edit_text('Шаг 1/4\n\nВведите название тарифа 👇', reply_markup=markup)
    await state.set_state(FsmTarifAdmin.get_name)


@router.message(StateFilter(FsmTarifAdmin.get_name))
async def get_name(message: types.Message, state: FSMContext):
    """Получение названия тарифа"""
    logging.info('get_name')
    name = str(message.text)
    markup = await tarifs_keyboard.back_button('back-to-add-tarif_name')
    await message.answer('Шаг 2/4\n\n'
                            'Введите цену тарифа 👇', reply_markup=markup)
    await state.set_state(FsmTarifAdmin.get_cost)
    await state.update_data(name=name)


@router.message(StateFilter(FsmTarifAdmin.get_cost))
async def get_cost(message: types.Message, state: FSMContext):
    """Получение цены тарифа"""
    logging.info('get_cost')
    cost = str(message.text)
    check_data = await utils.validate_int_data(cost)
    if check_data:
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_cost')
        await message.answer('Шаг 3/4\n\n'
                             'Введите кол-во сообщений для ИИ 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_message_cnt)
        await state.update_data(cost=int(cost))
    else:
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_name')
        await message.answer('Введена некорректная цена, попробуйте еще раз ❌', reply_markup=markup)


@router.message(StateFilter(FsmTarifAdmin.get_message_cnt))
async def get_message_cnt(message: types.Message, state: FSMContext):
    """Получение кол-ва сообщений"""
    logging.info('get_message_cnt')
    message_cnt = str(message.text)
    check_data = await utils.validate_int_data(message_cnt)

    if check_data:
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_message-cnt')
        await message.answer('Шаг 4/4\n\n'
                             'Отправьте фотографию для тарифа 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_photo)
        await state.update_data(message_cnt=int(message_cnt))
    else:
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_name')
        await message.answer('Введено некорректное кол-во сообщений, попробуйте еще раз ❌', reply_markup=markup)


@router.message(StateFilter(FsmTarifAdmin.get_photo))
async def get_photo(message: types.Message, state: FSMContext):
    """Получение фотографии"""
    logging.info('get_photo')
    if message.photo:
        file_id = message.photo[-1].file_id
        state_data = await state.get_data()
        await admin_requests.add_new_tarif(state_data['tarif_type'], state_data['name'], state_data['message_cnt'], file_id, state_data['cost'])
        await message.answer('Тариф успешно добавлен, теперь он доступен к настройкам в разделе "Редактировать тарифы ⚙️"')
        await state.clear()
        await state.set_state(default_state)
    else:
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_name')
        await message.answer('Вы отправили не фото/видео, попробуйте еще раз ❌', reply_markup=markup)


@router.callback_query(F.data.startswith('back-to-add-tarif_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопко назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]

    if flag == 'name':
        markup = await tarifs_keyboard.back_button('back-to-select-tarif-redact-admin')
        await callback.message.edit_text('Шаг 1/4\n\nВведите название тарифа 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_name)
    if flag == 'cost':
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_name')
        await callback.message.edit_text('Шаг 2/4\n\nВведите цену тарифа 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_cost)
    if flag == 'message-cnt':
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_cost')
        await callback.message.edit_text('Шаг 3/4\n\nВведите кол-во сообщений для ИИ 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_message_cnt)
    if flag == 'photo':
        markup = await tarifs_keyboard.back_button('back-to-add-tarif_message-cnt')
        await callback.message.edit_text('Шаг 4/4\n\nОтправьте фотографию для тарифа 👇', reply_markup=markup)
        await state.set_state(FsmTarifAdmin.get_photo)
    if flag == 'main-menu':
        state_data = await state.get_data()
        tarif_type = state_data['tarif_type']
        tarif_data = await admin_requests.get_tarif_type(tarif_type)
        markup = await tarifs_keyboard.tarif_settings()
        text = (f'📄 Название: {tarif_data["name"]}\n'
                f'💵 Цена: {tarif_data["cost"]}р\n'
                f'📩 Кол-во сообщений в день: {tarif_data["message_cnt"]}\n\n'
                f'Выберите параметр для изменения 👇')
        await callback.message.edit_caption(caption=text, reply_markup=markup)



















