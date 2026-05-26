from aiogram import Router, types, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
import logging

from aiogram.types import FSInputFile
from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import ai_token_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


@router.message(F.text == 'Выгрузка пользователей 👥')
async def users_handler(message: types.Message, state: FSMContext):
    """Выгрузка списка пользховатетлей"""
    logging.info('users_handler')
    users_data = await admin_requests.get_all_users_data()
    if users_data:
        await utils.create_users_table(users_data)
        await message.answer_document(document=FSInputFile('Пользователи.xlsx'))
    else:
        await message.answer('Ни один пользователь не зарегистрирован ❌')

    await state.clear()
