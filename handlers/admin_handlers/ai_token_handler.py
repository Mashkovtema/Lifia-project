from aiogram import Router, types, F, flags, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter, Command
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import ai_token_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


class FsmAiToken(StatesGroup):
    get_new_token = State()
    get_file = State()


@router.message(F.text == 'Ключ к ии моделям 🗝')
async def ai_token(message: types.Message, state: FSMContext):
    """Смена токена к моделям"""
    logging.info('ai_token')
    token = await admin_requests.get_token()
    markup = await ai_token_keyboard.change_token_button()
    text = (f'Текущий ключ к ии моделям: {token}\n\n'
            f'Нажмите на кнопку для смены ключа 👇')
    await message.answer(text=text, reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == 'back-to-ai-token-admin')
async def back_to_ai_token(callback: types.CallbackQuery, state: FSMContext):
    """Назал к токену"""
    logging.info('back_to_ai_token')
    token = await admin_requests.get_token()
    markup = await ai_token_keyboard.change_token_button()
    text = (f'Текущий ключ к ии моделям: {token}\n\n'
            f'Нажмите на кнопку для смены ключа 👇')
    await callback.message.edit_text(text=text, reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == 'change-token-admin')
async def change_ai_token(callback: types.CallbackQuery, state: FSMContext):
    """Смена ключа"""
    logging.info('change_ai_token')
    markup = await ai_token_keyboard.back_button()
    await callback.message.edit_text('Отправьте новый ключ 👇', reply_markup=markup)
    await state.set_state(FsmAiToken.get_new_token)


@router.message(StateFilter(FsmAiToken.get_new_token))
async def get_new_token(message: types.Message, state: FSMContext):
    """Получение нового токена"""
    logging.info('get_new_token')
    new_token = str(message.text)
    await admin_requests.update_ai_token(new_token)
    await message.answer('Ключ успешно обновлен ✅')
    await state.clear()


@router.message(Command('file'))
async def get_new_file(message: types.Message, state: FSMContext):
    """Запрос файла для обновления данных по текстам"""
    logging.info('get_new_file')
    markup = await ai_token_keyboard.file_type_buttons()
    await state.set_state(default_state)
    await message.answer('Выберите тип файла 👇', reply_markup=markup)


@router.callback_query(F.data.startswith('select-file-type_'))
async def select_file_type(callback: types.CallbackQuery, state: FSMContext):
    """Выбор типа файла"""
    logging.info('select_file_type')
    type = str(callback.data).split('_')[1]
    await state.set_state(FsmAiToken.get_file)
    await state.update_data(type=type)
    await callback.message.edit_text('Отправьте новый файл 👇')


@router.message(StateFilter(FsmAiToken.get_file))
async def update_texts_data(message: types.Message, state: FSMContext, bot: Bot):
    """ПОлучение файла и обработка данных"""
    logging.info('update_texts_data')
    document = message.document
    if not document.file_name.endswith(('.xlsx', '.xls')):
        await message.answer("Пожалуйста, отправьте файл Excel (.xlsx или .xls)")
    else:
        state_data = await state.get_data()
        file_in_memory = await message.bot.download(document)
        send_message = await message.answer('Обновление текстов ⏳ ...')
        await admin_requests.update_weeks_text(file_in_memory, state_data['type'])
        await state.set_state(default_state)
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=send_message.message_id,
                                    text='Тексты успешно обновлены ✅')









