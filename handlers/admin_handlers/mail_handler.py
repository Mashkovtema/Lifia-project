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


@router.message(F.text == 'Создать рассылку 🗝')
async def mail_handler(message: types.Message, state: FSMContext):
    """Рассылки"""
    logging.info('mail_handler')
    await state.clear()
    await message.answer('Тут будут рассылки')