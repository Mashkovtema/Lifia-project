from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
    
import logging
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import start_keyboard

from database.requests import admin_requests, user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')

def extract_arg(arg):
    return arg.split()[1:]


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    """Старт"""
    logging.info(f'start: {message.from_user.id}')
    user_id = int(message.from_user.id)

    if str(user_id) in admin_ids:
        markup = await start_keyboard.main_buttons()
        await message.answer('Вы администратор, выберите действие:', reply_markup=markup)
    else:
        pass

