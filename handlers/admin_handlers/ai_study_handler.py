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


@router.message(F.text == 'Обучение модели 🤖')
async def ai_study(message: types.Message, state: FSMContext):
    """Обучение модели"""
    logging.info('ai_study')
    await state.clear()
    await message.answer('Тут будет обучение модели')