from aiogram import Router, types, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
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














